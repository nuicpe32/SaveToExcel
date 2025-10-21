import React, { useState, useEffect } from 'react';
import { Modal, Table, Tag, Space, Typography, Empty } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';
import { lineService, NotificationLog } from '../services/lineService';

const { Text } = Typography;

interface LineNotificationHistoryModalProps {
  visible: boolean;
  onClose: () => void;
}

const LineNotificationHistoryModal: React.FC<LineNotificationHistoryModalProps> = ({
  visible,
  onClose,
}) => {
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState<NotificationLog[]>([]);

  useEffect(() => {
    if (visible) {
      fetchHistory();
    }
  }, [visible]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await lineService.getNotificationHistory(50);
      setLogs(data);
    } catch (error) {
      console.error('Error fetching notification history:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusTag = (status: string) => {
    switch (status) {
      case 'sent':
        return <Tag icon={<CheckCircleOutlined />} color="success">ส่งสำเร็จ</Tag>;
      case 'failed':
        return <Tag icon={<CloseCircleOutlined />} color="error">ส่งล้มเหลว</Tag>;
      case 'pending':
        return <Tag icon={<ClockCircleOutlined />} color="processing">กำลังส่ง</Tag>;
      default:
        return <Tag>{status}</Tag>;
    }
  };

  const getNotificationTypeText = (type: string) => {
    const typeMap: Record<string, string> = {
      connection_test: 'ทดสอบการเชื่อมต่อ',
      new_case: 'คดีใหม่',
      case_update: 'อัปเดตคดี',
      summons_sent: 'ส่งหมายเรียก',
      email_opened: 'เปิดอีเมล์',
    };
    return typeMap[type] || type;
  };

  const columns = [
    {
      title: 'วันที่/เวลา',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => new Date(date).toLocaleString('th-TH'),
    },
    {
      title: 'ประเภท',
      dataIndex: 'notification_type',
      key: 'notification_type',
      width: 140,
      render: (type: string) => getNotificationTypeText(type),
    },
    {
      title: 'หัวข้อ',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
    },
    {
      title: 'ข้อความ',
      dataIndex: 'message',
      key: 'message',
      ellipsis: true,
      render: (text: string) => (
        <Text style={{ fontSize: '12px' }}>
          {text.length > 100 ? `${text.substring(0, 100)}...` : text}
        </Text>
      ),
    },
    {
      title: 'สถานะ',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status: string) => getStatusTag(status),
    },
  ];

  return (
    <Modal
      title="ประวัติการแจ้งเตือน LINE"
      open={visible}
      onCancel={onClose}
      footer={null}
      width={1000}
    >
      <Table
        columns={columns}
        dataSource={logs}
        rowKey="id"
        loading={loading}
        pagination={{
          pageSize: 10,
          showSizeChanger: false,
          showTotal: (total) => `ทั้งหมด ${total} รายการ`,
        }}
        locale={{
          emptyText: (
            <Empty
              description="ยังไม่มีประวัติการแจ้งเตือน"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          ),
        }}
        expandable={{
          expandedRowRender: (record) => (
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Text strong>ข้อความเต็ม:</Text>
                <div style={{ marginTop: '8px', whiteSpace: 'pre-wrap' }}>
                  {record.message}
                </div>
              </div>
              {record.sent_at && (
                <div>
                  <Text strong>ส่งเมื่อ:</Text> {new Date(record.sent_at).toLocaleString('th-TH')}
                </div>
              )}
              {record.error_message && (
                <div>
                  <Text strong type="danger">ข้อผิดพลาด:</Text>
                  <div style={{ marginTop: '4px', color: '#ff4d4f' }}>
                    {record.error_message}
                  </div>
                </div>
              )}
            </Space>
          ),
          rowExpandable: (record) => !!record.message || !!record.error_message,
        }}
      />
    </Modal>
  );
};

export default LineNotificationHistoryModal;
