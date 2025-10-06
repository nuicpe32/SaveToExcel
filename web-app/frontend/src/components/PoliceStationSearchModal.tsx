import React, { useState } from 'react';
import {
  Modal,
  Button,
  Spin,
  Alert,
  List,
  Typography,
  Space,
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
  id: number;
  station_name: string;
  station_code?: string;
  province: string;
  district?: string;
  subdistrict?: string;
  address?: string;
  postal_code?: string;
  phone?: string;
  subdistricts_covered?: string;
  created_at?: string;
  updated_at?: string;
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
  const [warningMessage, setWarningMessage] = useState<string>('');

  const handleSearch = async () => {
    if (!suspectAddress.trim()) {
      setError('กรุณากรอกที่อยู่ของผู้ต้องหาก่อน');
      return;
    }

    setLoading(true);
    setError('');
    setWarningMessage('');
    setSearchResults([]);

    try {
      // ส่งคำขอไปยัง backend เพื่อค้นหาสถานีตำรวจ
      const response = await api.post('/police-stations/search', {
        address: suspectAddress,
      });

      console.log('API Response:', response.data);

      if (response.data) {
        const data = response.data;
        let stations: PoliceStation[] = [];

        // ตรวจสอบ exact match ก่อน
        if (data.exact_match) {
          stations.push(data.exact_match);
        }

        // ตรวจสอบ district matches
        if (data.district_matches && data.district_matches.length > 0) {
          stations = stations.concat(data.district_matches);
        }

        // ตรวจสอบ province matches
        if (data.province_matches && data.province_matches.length > 0) {
          stations = stations.concat(data.province_matches);
        }

        setSearchResults(stations);
        
        // ตรวจสอบการแจ้งเตือนจาก backend
        if (data.has_incomplete_address && data.warning_message) {
          setWarningMessage(data.warning_message);
        }
        
        if (stations.length === 0) {
          setError('ไม่พบสถานีตำรวจในพื้นที่นี้');
        }
      } else {
        setError('ไม่สามารถค้นหาสถานีตำรวจได้');
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

        {warningMessage && (
          <Alert
            message="⚠️ ข้อมูลไม่สมบูรณ์"
            description={warningMessage}
            type="warning"
            showIcon
            style={{ marginTop: 8 }}
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
                        <Text strong>{station.station_name}</Text>
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
                        <Text>{station.address || 'ไม่มีข้อมูลที่อยู่'}</Text>
                        <br />
                        <Text type="secondary">
                          {station.district && station.district + ', '}{station.province}
                        </Text>
                        {station.subdistricts_covered && (
                          <>
                            <br />
                            <Text type="secondary" style={{ fontSize: 12 }}>
                              พื้นที่รับผิดชอบ: {station.subdistricts_covered}
                            </Text>
                          </>
                        )}
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
