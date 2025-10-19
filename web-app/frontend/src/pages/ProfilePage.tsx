import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, Upload, message, Avatar, Space, Typography, Divider } from 'antd';
import { UserOutlined, UploadOutlined, DeleteOutlined, SaveOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import axios from 'axios';
import { useAuthStore } from '../stores/authStore';

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
  const { token } = useAuthStore();

  useEffect(() => {
    if (token) {
      fetchProfile();
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
        </Space>
      </Card>
    </div>
  );
};

export default ProfilePage;
