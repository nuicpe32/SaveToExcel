import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, Upload, message, Avatar, Space, Typography, Divider, Switch, Badge, Modal } from 'antd';
import { UserOutlined, UploadOutlined, DeleteOutlined, SaveOutlined, LineOutlined, BellOutlined, DisconnectOutlined, HistoryOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import axios from 'axios';
import { useAuthStore } from '../stores/authStore';
import { lineService, LineStatus } from '../services/lineService';
import LineNotificationHistoryModal from '../components/LineNotificationHistoryModal';

const { Title, Text } = Typography;

interface UserProfile {
  id: number;
  username: string;
  email: string;
  full_name: string;
  position?: string;
  phone_number?: string;
  line_id?: string;
  signature_path?: string;
  has_signature: boolean;
}

const ProfilePage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [signaturePreview, setSignaturePreview] = useState<string | null>(null);
  const [lineStatus, setLineStatus] = useState<LineStatus | null>(null);
  const [lineLoading, setLineLoading] = useState(false);
  const [historyModalVisible, setHistoryModalVisible] = useState(false);
  const { token } = useAuthStore();

  useEffect(() => {
    if (token) {
      fetchProfile();
      fetchLineStatus();
    }
  }, [token]);

  const fetchProfile = async () => {
    try {
      const response = await axios.get('/api/v1/profile/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProfile(response.data);
      form.setFieldsValue(response.data);

      // Set signature preview
      if (response.data.signature_path) {
        setSignaturePreview(`http://localhost:8000/uploads/${response.data.signature_path}`);
      }
    } catch (error: any) {
      message.error('ไม่สามารถโหลดข้อมูลโปรไฟล์ได้');
      console.error(error);
    }
  };

  const handleUpdateProfile = async (values: any) => {
    setLoading(true);
    try {
      const response = await axios.put('/api/v1/profile/me', values, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProfile(response.data);
      message.success('อัปเดตข้อมูลโปรไฟล์สำเร็จ');
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'ไม่สามารถอัปเดตข้อมูลได้');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const uploadProps: UploadProps = {
    name: 'file',
    accept: '.png',
    maxCount: 1,
    showUploadList: false,
    beforeUpload: (file) => {
      const isPNG = file.type === 'image/png';
      if (!isPNG) {
        message.error('อัปโหลดได้เฉพาะไฟล์ PNG เท่านั้น!');
        return false;
      }
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        message.error('ขนาดไฟล์ต้องไม่เกิน 2MB!');
        return false;
      }
      return true;
    },
    customRequest: async ({ file, onSuccess, onError }) => {
      setUploadLoading(true);
      try {
        const formData = new FormData();
        formData.append('file', file as File);

        const response = await axios.post('/api/v1/profile/me/signature', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });

        message.success('อัปโหลดลายเซ็นสำเร็จ');
        await fetchProfile();
        onSuccess?.(response.data);
      } catch (error: any) {
        message.error(error.response?.data?.detail || 'ไม่สามารถอัปโหลดไฟล์ได้');
        onError?.(error);
      } finally {
        setUploadLoading(false);
      }
    }
  };

  const handleDeleteSignature = async () => {
    try {
      await axios.delete('/api/v1/profile/me/signature', {
        headers: { Authorization: `Bearer ${token}` }
      });
      message.success('ลบลายเซ็นสำเร็จ');
      setSignaturePreview(null);
      await fetchProfile();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'ไม่สามารถลบลายเซ็นได้');
      console.error(error);
    }
  };

  const fetchLineStatus = async () => {
    try {
      const status = await lineService.getStatus();
      setLineStatus(status);
    } catch (error: any) {
      console.error('Error fetching LINE status:', error);
    }
  };

  const handleConnectLine = async () => {
    setLineLoading(true);
    try {
      const authUrl = await lineService.getAuthUrl();
      window.location.href = authUrl;
    } catch (error: any) {
      message.error('ไม่สามารถเชื่อมต่อ LINE ได้');
      console.error(error);
    } finally {
      setLineLoading(false);
    }
  };

  const handleDisconnectLine = () => {
    Modal.confirm({
      title: 'ยกเลิกการเชื่อมต่อ LINE',
      content: 'คุณแน่ใจหรือไม่ว่าต้องการยกเลิกการเชื่อมต่อบัญชี LINE?',
      okText: 'ยกเลิกการเชื่อมต่อ',
      cancelText: 'ปิด',
      okButtonProps: { danger: true },
      onOk: async () => {
        try {
          await lineService.disconnect();
          message.success('ยกเลิกการเชื่อมต่อสำเร็จ');
          await fetchLineStatus();
        } catch (error: any) {
          message.error('ไม่สามารถยกเลิกการเชื่อมต่อได้');
          console.error(error);
        }
      },
    });
  };

  const handlePreferenceChange = async (key: string, value: boolean) => {
    try {
      await lineService.updatePreferences({ [key]: value });
      message.success('อัปเดตการตั้งค่าสำเร็จ');
      await fetchLineStatus();
    } catch (error: any) {
      message.error('ไม่สามารถอัปเดตการตั้งค่าได้');
      console.error(error);
    }
  };

  const handleTestNotification = async () => {
    try {
      await lineService.sendTestNotification();
      message.success('ส่งการแจ้งเตือนทดสอบสำเร็จ กรุณาตรวจสอบ LINE ของคุณ');
    } catch (error: any) {
      message.error('ไม่สามารถส่งการแจ้งเตือนได้');
      console.error(error);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Title level={2}>
              <UserOutlined /> โปรไฟล์ส่วนตัว
            </Title>
            <Text type="secondary">
              จัดการข้อมูลส่วนตัวและลายเซ็นของคุณ
            </Text>
          </div>

          <Divider />

          {/* Profile Information Form */}
          <Card title="ข้อมูลส่วนตัว" size="small">
            <Form
              form={form}
              layout="vertical"
              onFinish={handleUpdateProfile}
              autoComplete="off"
            >
              <Form.Item
                label="ชื่อผู้ใช้งาน"
                name="username"
              >
                <Input disabled />
              </Form.Item>

              <Form.Item
                label="ชื่อ-นามสกุล"
                name="full_name"
                rules={[{ required: true, message: 'กรุณากรอกชื่อ-นามสกุล' }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="อีเมล"
                name="email"
                rules={[
                  { required: true, message: 'กรุณากรอกอีเมล' },
                  { type: 'email', message: 'รูปแบบอีเมลไม่ถูกต้อง' }
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="ตำแหน่ง"
                name="position"
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="เบอร์โทรศัพท์"
                name="phone_number"
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="LINE ID"
                name="line_id"
              >
                <Input />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  icon={<SaveOutlined />}
                  loading={loading}
                >
                  บันทึกข้อมูล
                </Button>
              </Form.Item>
            </Form>
          </Card>

          {/* Signature Upload */}
          <Card title="ลายเซ็นอิเล็กทรอนิกส์" size="small">
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <div>
                <Text type="secondary">
                  อัปโหลดลายเซ็นของคุณ (ไฟล์ PNG เท่านั้น, ขนาดไม่เกิน 2MB)
                  <br />
                  ลายเซ็นจะถูกนำไปใช้ในเอกสารหมายเรียกอัตโนมัติ
                </Text>
              </div>

              {signaturePreview ? (
                <Space direction="vertical" align="center" style={{ width: '100%' }}>
                  <div
                    style={{
                      border: '1px solid #d9d9d9',
                      borderRadius: '4px',
                      padding: '16px',
                      backgroundColor: '#fafafa',
                      textAlign: 'center'
                    }}
                  >
                    <img
                      src={signaturePreview}
                      alt="ลายเซ็น"
                      style={{ maxWidth: '300px', maxHeight: '150px' }}
                    />
                  </div>
                  <Space>
                    <Upload {...uploadProps}>
                      <Button icon={<UploadOutlined />} loading={uploadLoading}>
                        เปลี่ยนลายเซ็น
                      </Button>
                    </Upload>
                    <Button
                      danger
                      icon={<DeleteOutlined />}
                      onClick={handleDeleteSignature}
                    >
                      ลบลายเซ็น
                    </Button>
                  </Space>
                </Space>
              ) : (
                <Upload {...uploadProps}>
                  <Button icon={<UploadOutlined />} loading={uploadLoading}>
                    อัปโหลดลายเซ็น (PNG)
                  </Button>
                </Upload>
              )}
            </Space>
          </Card>

          {/* LINE Integration */}
          <Card
            title={
              <Space>
                <LineOutlined style={{ color: '#00B900' }} />
                <span>การเชื่อมต่อ LINE</span>
                {lineStatus?.connected && (
                  <Badge status="success" text="เชื่อมต่อแล้ว" />
                )}
              </Space>
            }
            size="small"
          >
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              {lineStatus?.connected ? (
                <>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {lineStatus.line_picture_url && (
                      <Avatar src={lineStatus.line_picture_url} size={48} />
                    )}
                    <div>
                      <div style={{ fontWeight: 500 }}>{lineStatus.line_display_name}</div>
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        เชื่อมต่อเมื่อ: {lineStatus.linked_at ? new Date(lineStatus.linked_at).toLocaleString('th-TH') : '-'}
                      </Text>
                    </div>
                  </div>

                  <Divider style={{ margin: '8px 0' }} />

                  <div>
                    <Text strong><BellOutlined /> การตั้งค่าการแจ้งเตือน</Text>
                    <div style={{ marginTop: '12px' }}>
                      <Space direction="vertical" style={{ width: '100%' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Text>แจ้งเตือนคดีใหม่</Text>
                          <Switch
                            checked={lineStatus.notify_new_case}
                            onChange={(checked) => handlePreferenceChange('notify_new_case', checked)}
                          />
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Text>แจ้งเตือนอัปเดตคดี</Text>
                          <Switch
                            checked={lineStatus.notify_case_update}
                            onChange={(checked) => handlePreferenceChange('notify_case_update', checked)}
                          />
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Text>แจ้งเตือนส่งหมายเรียก</Text>
                          <Switch
                            checked={lineStatus.notify_summons_sent}
                            onChange={(checked) => handlePreferenceChange('notify_summons_sent', checked)}
                          />
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Text>แจ้งเตือนเปิดอีเมล์</Text>
                          <Switch
                            checked={lineStatus.notify_email_opened}
                            onChange={(checked) => handlePreferenceChange('notify_email_opened', checked)}
                          />
                        </div>
                      </Space>
                    </div>
                  </div>

                  <Divider style={{ margin: '8px 0' }} />

                  <Space wrap>
                    <Button
                      icon={<BellOutlined />}
                      onClick={handleTestNotification}
                    >
                      ทดสอบการแจ้งเตือน
                    </Button>
                    <Button
                      icon={<HistoryOutlined />}
                      onClick={() => setHistoryModalVisible(true)}
                    >
                      ประวัติการแจ้งเตือน
                    </Button>
                    <Button
                      danger
                      icon={<DisconnectOutlined />}
                      onClick={handleDisconnectLine}
                    >
                      ยกเลิกการเชื่อมต่อ
                    </Button>
                  </Space>
                </>
              ) : (
                <>
                  <div>
                    <Text type="secondary">
                      เชื่อมต่อบัญชี LINE ของคุณเพื่อรับการแจ้งเตือนสำคัญผ่าน LINE
                      <br />
                      <br />
                      คุณจะได้รับการแจ้งเตือนเมื่อ:
                    </Text>
                    <ul style={{ marginTop: '8px', marginBottom: '16px' }}>
                      <li>มีคดีใหม่ที่ได้รับมอบหมาย</li>
                      <li>มีการอัปเดตข้อมูลคดี</li>
                      <li>ส่งหมายเรียกสำเร็จ</li>
                      <li>ผู้ต้องหาเปิดอ่านอีเมล์หมายเรียก</li>
                    </ul>
                  </div>
                  <Button
                    type="primary"
                    icon={<LineOutlined />}
                    onClick={handleConnectLine}
                    loading={lineLoading}
                    style={{ backgroundColor: '#00B900', borderColor: '#00B900' }}
                  >
                    เชื่อมต่อบัญชี LINE
                  </Button>
                </>
              )}
            </Space>
          </Card>
        </Space>
      </Card>

      <LineNotificationHistoryModal
        visible={historyModalVisible}
        onClose={() => setHistoryModalVisible(false)}
      />
    </div>
  );
};

export default ProfilePage;
