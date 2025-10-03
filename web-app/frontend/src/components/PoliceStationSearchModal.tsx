import React, { useState } from 'react';
import {
  Modal,
  Input,
  Button,
  Spin,
  Alert,
  List,
  Typography,
  Space,
  Divider,
} from 'antd';
import {
  SearchOutlined,
  EnvironmentOutlined,
  PhoneOutlined,
  CheckOutlined,
} from '@ant-design/icons';
import api from '../services/api';

const { Text, Title } = Typography;

interface PoliceStation {
  name: string;
  address: string;
  phone?: string;
  district: string;
  province: string;
}

interface PoliceStationSearchModalProps {
  visible: boolean;
  onCancel: () => void;
  onSelect: (station: PoliceStation) => void;
  suspectAddress: string;
}

const PoliceStationSearchModal: React.FC<PoliceStationSearchModalProps> = ({
  visible,
  onCancel,
  onSelect,
  suspectAddress,
}) => {
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<PoliceStation[]>([]);
  const [error, setError] = useState<string>('');

  const handleSearch = async () => {
    if (!suspectAddress.trim()) {
      setError('กรุณากรอกที่อยู่ของผู้ต้องหาก่อน');
      return;
    }

    setLoading(true);
    setError('');
    setSearchResults([]);

    try {
      // ส่งคำขอไปยัง backend เพื่อค้นหาสถานีตำรวจ
      const response = await api.post('/police-stations/search', {
        address: suspectAddress,
      });

      if (response.data && response.data.success) {
        setSearchResults(response.data.stations || []);
        if (!response.data.stations || response.data.stations.length === 0) {
          setError('ไม่พบสถานีตำรวจในพื้นที่นี้');
        }
      } else {
        setError(response.data?.message || 'ไม่สามารถค้นหาสถานีตำรวจได้');
      }
    } catch (err: any) {
      setError('เกิดข้อผิดพลาดในการค้นหาสถานีตำรวจ');
      console.error('Police station search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectStation = (station: PoliceStation) => {
    onSelect(station);
    onCancel();
  };

  return (
    <Modal
      title={
        <Space>
          <SearchOutlined />
          <span>ค้นหาสถานีตำรวจในพื้นที่รับผิดชอบ</span>
        </Space>
      }
      open={visible}
      onCancel={onCancel}
      footer={null}
      width={800}
      destroyOnClose
    >
      <div style={{ marginBottom: 16 }}>
        <Text strong>ที่อยู่ของผู้ต้องหา:</Text>
        <br />
        <Text code style={{ fontSize: 14, marginTop: 4, display: 'inline-block' }}>
          {suspectAddress || '(ยังไม่ได้กรอกที่อยู่)'}
        </Text>
      </div>

      <Space direction="vertical" style={{ width: '100%' }}>
        <Button
          type="primary"
          icon={<SearchOutlined />}
          onClick={handleSearch}
          loading={loading}
          disabled={!suspectAddress.trim()}
          block
        >
          ค้นหาสถานีตำรวจ
        </Button>

        {error && (
          <Alert
            message="ไม่สามารถค้นหาได้"
            description={error}
            type="error"
            showIcon
          />
        )}

        {loading && (
          <div style={{ textAlign: 'center', padding: 20 }}>
            <Spin size="large" />
            <div style={{ marginTop: 8 }}>
              <Text>กำลังค้นหาสถานีตำรวจในพื้นที่...</Text>
            </div>
          </div>
        )}

        {searchResults.length > 0 && (
          <div>
            <Title level={5}>ผลการค้นหา ({searchResults.length} แห่ง)</Title>
            <List
              dataSource={searchResults}
              renderItem={(station) => (
                <List.Item
                  actions={[
                    <Button
                      type="primary"
                      icon={<CheckOutlined />}
                      onClick={() => handleSelectStation(station)}
                      size="small"
                    >
                      เลือก
                    </Button>,
                  ]}
                >
                  <List.Item.Meta
                    avatar={<EnvironmentOutlined style={{ fontSize: 24, color: '#1890ff' }} />}
                    title={
                      <Space>
                        <Text strong>{station.name}</Text>
                        {station.phone && (
                          <Space size="small">
                            <PhoneOutlined />
                            <Text type="secondary">{station.phone}</Text>
                          </Space>
                        )}
                      </Space>
                    }
                    description={
                      <div>
                        <Text>{station.address}</Text>
                        <br />
                        <Text type="secondary">
                          {station.district}, {station.province}
                        </Text>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </div>
        )}
      </Space>
    </Modal>
  );
};

export default PoliceStationSearchModal;
