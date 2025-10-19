import React, { useEffect, useState } from 'react';
import {
  Modal,
  Table,
  Tag,
  Space,
  Typography,
  Alert,
  Tooltip,
  Badge,
  Card,
  Statistic,
  Row,
  Col,
  Divider,
  Empty
} from 'antd';
import {
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  MailOutlined,
  EyeOutlined,
  RedoOutlined,
  WarningOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';
import 'dayjs/locale/th';
import buddhistEra from 'dayjs/plugin/buddhistEra';
import relativeTime from 'dayjs/plugin/relativeTime';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import api from '../services/api';

dayjs.extend(buddhistEra);
dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale('th');

// Set default timezone to Bangkok
dayjs.tz.setDefault('Asia/Bangkok');

const { Title, Text } = Typography;

interface EmailLog {
  id: number;
  account_type: string;
  account_id: number;
  criminal_case_id: number;
  recipient_email: string;
  subject: string;
  document_type: string;
  status: 'sent' | 'failed' | 'pending';
  sent_at: string | null;
  error_message: string | null;
  retry_count: number;
  opened_count: number;
  created_at: string;
  pdf_filename: string | null;
}

interface EmailHistoryModalProps {
  visible: boolean;
  onClose: () => void;
  accountType: 'non_bank' | 'payment_gateway' | 'telco_mobile' | 'telco_internet' | 'bank';
  accountId: number;
  accountInfo?: {
    documentNumber?: string;
    providerName?: string;
    accountNumber?: string;
  };
}

const EmailHistoryModal: React.FC<EmailHistoryModalProps> = ({
  visible,
  onClose,
  accountType,
  accountId,
  accountInfo
}) => {
  const [emailLogs, setEmailLogs] = useState<EmailLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);

  // แปล account_type เป็นภาษาไทย
  const getAccountTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'non_bank': 'Non-Bank',
      'payment_gateway': 'Payment Gateway',
      'telco_mobile': 'หมายเลขโทรศัพท์',
      'telco_internet': 'IP Address',
      'bank': 'บัญชีธนาคาร'
    };
    return labels[type] || type;
  };

  // โหลดข้อมูล
  const fetchEmailLogs = async () => {
    if (!accountId || !accountType) return;
    
    setLoading(true);
    try {
      const response = await api.get(`/emails/by-account/${accountType}/${accountId}`);
      setEmailLogs(response.data.emails);
      setTotal(response.data.total);
    } catch (error) {
      console.error('Error fetching email logs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (visible && accountId && accountType) {
      fetchEmailLogs();
    }
  }, [visible, accountId, accountType]);

  // Status Tag
  const getStatusTag = (status: string) => {
    const configs: Record<string, { color: string; icon: React.ReactNode; text: string }> = {
      sent: {
        color: 'success',
        icon: <CheckCircleOutlined />,
        text: 'ส่งสำเร็จ'
      },
      failed: {
        color: 'error',
        icon: <CloseCircleOutlined />,
        text: 'ส่งไม่สำเร็จ'
      },
      pending: {
        color: 'warning',
        icon: <ClockCircleOutlined />,
        text: 'กำลังส่ง'
      }
    };

    const config = configs[status] || configs.pending;
    return (
      <Tag color={config.color} icon={config.icon}>
        {config.text}
      </Tag>
    );
  };

  // สถิติการส่งอีเมล์
  const getStatistics = () => {
    const sent = emailLogs.filter(log => log.status === 'sent').length;
    const failed = emailLogs.filter(log => log.status === 'failed').length;
    const pending = emailLogs.filter(log => log.status === 'pending').length;
    const totalOpened = emailLogs.reduce((sum, log) => sum + log.opened_count, 0);

    return { sent, failed, pending, totalOpened };
  };

  const stats = getStatistics();

  // Columns สำหรับตาราง
  const columns = [
    {
      title: 'วันที่ส่ง',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => {
        // แปลงจาก UTC เป็น Bangkok timezone
        const time = dayjs.utc(date).tz('Asia/Bangkok');
        return (
          <Space direction="vertical" size={0}>
            <Text strong>{time.format('DD/MM/BBBB')}</Text>
            <Text type="secondary" style={{ fontSize: '12px' }}>
              {time.format('HH:mm:ss น.')}
            </Text>
            <Text type="secondary" style={{ fontSize: '11px' }}>
              ({time.fromNow()})
            </Text>
          </Space>
        );
      }
    },
    {
      title: 'ผู้รับ',
      dataIndex: 'recipient_email',
      key: 'recipient_email',
      width: 220,
      render: (email: string) => (
        <Tooltip title={email}>
          <Space>
            <MailOutlined style={{ color: '#1890ff' }} />
            <Text copyable={{ text: email }} ellipsis style={{ maxWidth: 180 }}>
              {email}
            </Text>
          </Space>
        </Tooltip>
      )
    },
    {
      title: 'สถานะ',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      align: 'center' as const,
      render: (status: string) => getStatusTag(status)
    },
    {
      title: 'การติดตาม',
      key: 'tracking',
      width: 150,
      align: 'center' as const,
      render: (_: any, record: EmailLog) => (
        <Space direction="vertical" size={2}>
          {record.status === 'sent' && (
            <>
              <Badge
                count={record.opened_count}
                showZero
                color={record.opened_count > 0 ? 'green' : 'gray'}
                style={{ fontSize: '11px' }}
              >
                <Tag icon={<EyeOutlined />} color={record.opened_count > 0 ? 'success' : 'default'}>
                  เปิดอ่าน
                </Tag>
              </Badge>
              {record.sent_at && (
                <Text type="secondary" style={{ fontSize: '11px' }}>
                  ส่งเมื่อ: {dayjs.utc(record.sent_at).tz('Asia/Bangkok').format('HH:mm')}
                </Text>
              )}
            </>
          )}
          {record.status === 'failed' && record.retry_count > 0 && (
            <Tag icon={<RedoOutlined />} color="orange">
              ลองใหม่ {record.retry_count} ครั้ง
            </Tag>
          )}
        </Space>
      )
    },
    {
      title: 'ไฟล์ PDF',
      dataIndex: 'pdf_filename',
      key: 'pdf_filename',
      width: 150,
      render: (filename: string | null) => (
        filename ? (
          <Tooltip title={filename}>
            <Tag icon={<FileTextOutlined />} color="blue">
              มีไฟล์แนบ
            </Tag>
          </Tooltip>
        ) : (
          <Text type="secondary">-</Text>
        )
      )
    },
    {
      title: 'ข้อผิดพลาด',
      dataIndex: 'error_message',
      key: 'error_message',
      width: 250,
      render: (error: string | null, record: EmailLog) => {
        if (record.status === 'failed' && error) {
          return (
            <Tooltip title={error}>
              <Alert
                message="ส่งไม่สำเร็จ"
                description={
                  <Text ellipsis style={{ maxWidth: 200 }}>
                    {error}
                  </Text>
                }
                type="error"
                showIcon
                icon={<WarningOutlined />}
                style={{ padding: '4px 8px', fontSize: '12px' }}
              />
            </Tooltip>
          );
        }
        return <Text type="secondary">-</Text>;
      }
    }
  ];

  return (
    <Modal
      title={
        <Space direction="vertical" size={0}>
          <Title level={4} style={{ margin: 0 }}>
            📧 ประวัติการส่งอีเมล์
          </Title>
          <Text type="secondary">
            {getAccountTypeLabel(accountType)}
            {accountInfo?.documentNumber && ` - ${accountInfo.documentNumber}`}
          </Text>
          {accountInfo?.providerName && (
            <Text type="secondary" style={{ fontSize: '13px' }}>
              {accountInfo.providerName}
              {accountInfo?.accountNumber && ` (${accountInfo.accountNumber})`}
            </Text>
          )}
        </Space>
      }
      open={visible}
      onCancel={onClose}
      width={1200}
      footer={null}
      destroyOnClose
    >
      {/* สถิติการส่งอีเมล์ */}
      {emailLogs.length > 0 && (
        <>
          <Row gutter={16} style={{ marginBottom: 24 }}>
            <Col span={6}>
              <Card>
                <Statistic
                  title="ส่งทั้งหมด"
                  value={total}
                  prefix={<MailOutlined />}
                  valueStyle={{ color: '#1890ff' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="ส่งสำเร็จ"
                  value={stats.sent}
                  prefix={<CheckCircleOutlined />}
                  valueStyle={{ color: '#52c41a' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="ส่งไม่สำเร็จ"
                  value={stats.failed}
                  prefix={<CloseCircleOutlined />}
                  valueStyle={{ color: '#ff4d4f' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="เปิดอ่านแล้ว"
                  value={stats.totalOpened}
                  prefix={<EyeOutlined />}
                  valueStyle={{ color: '#722ed1' }}
                />
              </Card>
            </Col>
          </Row>
          <Divider />
        </>
      )}

      {/* ตารางแสดงประวัติ */}
      <Table
        columns={columns}
        dataSource={emailLogs}
        rowKey="id"
        loading={loading}
        pagination={{
          pageSize: 10,
          showTotal: (total) => `ทั้งหมด ${total} รายการ`,
          showSizeChanger: true,
          pageSizeOptions: ['10', '20', '50', '100']
        }}
        locale={{
          emptyText: (
            <Empty
              image={Empty.PRESENTED_IMAGE_SIMPLE}
              description="ยังไม่มีประวัติการส่งอีเมล์"
            >
              <Text type="secondary">
                เมื่อมีการส่งหมายเรียกทางอีเมล์ ประวัติจะแสดงที่นี่
              </Text>
            </Empty>
          )
        }}
        scroll={{ x: 1100 }}
        size="middle"
        bordered
        rowClassName={(record) => {
          if (record.status === 'sent') return 'row-success';
          if (record.status === 'failed') return 'row-error';
          return '';
        }}
      />

      {/* คำอธิบายสถานะ */}
      {emailLogs.length > 0 && (
        <Alert
          message="คำอธิบายสถานะ"
          description={
            <Space direction="vertical" size={4}>
              <Text><CheckCircleOutlined style={{ color: '#52c41a' }} /> <strong>ส่งสำเร็จ:</strong> อีเมล์ถูกส่งไปยังผู้รับเรียบร้อยแล้ว</Text>
              <Text><CloseCircleOutlined style={{ color: '#ff4d4f' }} /> <strong>ส่งไม่สำเร็จ:</strong> เกิดข้อผิดพลาดในการส่ง (ดูรายละเอียดในคอลัมน์ข้อผิดพลาด)</Text>
              <Text><EyeOutlined style={{ color: '#722ed1' }} /> <strong>เปิดอ่าน:</strong> ผู้รับเปิดอ่านอีเมล์แล้ว (ถ้ารองรับ email tracking)</Text>
              <Text><RedoOutlined style={{ color: '#fa8c16' }} /> <strong>ลองใหม่:</strong> จำนวนครั้งที่พยายามส่งใหม่</Text>
            </Space>
          }
          type="info"
          showIcon
          style={{ marginTop: 16 }}
        />
      )}

      <style>
        {`
          .row-success {
            background-color: #f6ffed !important;
          }
          .row-error {
            background-color: #fff2f0 !important;
          }
          .row-success:hover,
          .row-error:hover {
            opacity: 0.9;
          }
        `}
      </style>
    </Modal>
  );
};

export default EmailHistoryModal;

