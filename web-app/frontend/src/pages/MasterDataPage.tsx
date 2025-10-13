import React, { useState, useEffect, useCallback } from 'react'
import {
  Table,
  Button,
  Space,
  message,
  Modal,
  Form,
  Input,
  Select,
  Popconfirm,
  Typography,
  Card,
  Tabs,
  Switch,
  DatePicker
} from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  BankOutlined,
  ShopOutlined,
  CreditCardOutlined,
  MobileOutlined,
  GlobalOutlined,
  SwapOutlined
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'
import dayjs from 'dayjs'

const { Title } = Typography
const { TextArea } = Input

interface Bank {
  id: number
  bank_name: string
  bank_code?: string
  bank_short_name?: string
  bank_address?: string
  soi?: string
  moo?: string
  road?: string
  sub_district?: string
  district?: string
  province?: string
  postal_code?: string
  created_at: string
  updated_at: string
}

interface NonBank {
  id: number
  company_name: string
  company_name_short?: string
  company_address?: string
  soi?: string
  moo?: string
  road?: string
  sub_district?: string
  district?: string
  province?: string
  postal_code?: string
  phone?: string
  email?: string
  website?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface PaymentGateway {
  id: number
  company_name: string
  company_name_short?: string
  company_address?: string
  soi?: string
  moo?: string
  road?: string
  sub_district?: string
  district?: string
  province?: string
  postal_code?: string
  phone?: string
  email?: string
  website?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface TelcoMobile {
  id: number
  company_name: string
  company_name_short?: string
  building_name?: string
  company_address?: string
  soi?: string
  moo?: string
  road?: string
  sub_district?: string
  district?: string
  province?: string
  postal_code?: string
  phone?: string
  email?: string
  website?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface TelcoInternet {
  id: number
  company_name: string
  company_name_short?: string
  building_name?: string
  company_address?: string
  soi?: string
  moo?: string
  road?: string
  sub_district?: string
  district?: string
  province?: string
  postal_code?: string
  phone?: string
  email?: string
  website?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface Exchange {
  id: number
  company_name: string
  company_name_short?: string
  company_name_alt?: string
  building_name?: string
  company_address?: string
  floor?: string
  unit?: string
  soi?: string
  moo?: string
  road?: string
  sub_district?: string
  district?: string
  province?: string
  postal_code?: string
  phone?: string
  email?: string
  website?: string
  license_number?: string
  license_date?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

type MasterDataType = Bank | NonBank | PaymentGateway | TelcoMobile | TelcoInternet | Exchange

export default function MasterDataPage() {
  const [banks, setBanks] = useState<Bank[]>([])
  const [nonBanks, setNonBanks] = useState<NonBank[]>([])
  const [paymentGateways, setPaymentGateways] = useState<PaymentGateway[]>([])
  const [telcoMobile, setTelcoMobile] = useState<TelcoMobile[]>([])
  const [telcoInternet, setTelcoInternet] = useState<TelcoInternet[]>([])
  const [exchanges, setExchanges] = useState<Exchange[]>([])

  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingItem, setEditingItem] = useState<MasterDataType | null>(null)
  const [currentDataType, setCurrentDataType] = useState<string>('banks')
  const [form] = Form.useForm()

  const fetchBanks = useCallback(async () => {
    try {
      const response = await api.get('/master-data/banks')
      setBanks(response.data)
    } catch (error: any) {
      message.error('ไม่สามารถดึงข้อมูลธนาคารได้')
    }
  }, [])

  const fetchNonBanks = useCallback(async () => {
    try {
      const response = await api.get('/master-data/non-banks')
      setNonBanks(response.data)
    } catch (error: any) {
      message.error('ไม่สามารถดึงข้อมูล Non-Bank ได้')
    }
  }, [])

  const fetchPaymentGateways = useCallback(async () => {
    try {
      const response = await api.get('/master-data/payment-gateways')
      setPaymentGateways(response.data)
    } catch (error: any) {
      message.error('ไม่สามารถดึงข้อมูล Payment Gateway ได้')
    }
  }, [])

  const fetchTelcoMobile = useCallback(async () => {
    try {
      const response = await api.get('/master-data/telco-mobile')
      setTelcoMobile(response.data)
    } catch (error: any) {
      message.error('ไม่สามารถดึงข้อมูลผู้ให้บริการโทรศัพท์มือถือได้')
    }
  }, [])

  const fetchTelcoInternet = useCallback(async () => {
    try {
      const response = await api.get('/master-data/telco-internet')
      setTelcoInternet(response.data)
    } catch (error: any) {
      message.error('ไม่สามารถดึงข้อมูลผู้ให้บริการอินเทอร์เน็ตได้')
    }
  }, [])

  const fetchExchanges = useCallback(async () => {
    try {
      const response = await api.get('/master-data/exchanges')
      setExchanges(response.data)
    } catch (error: any) {
      message.error('ไม่สามารถดึงข้อมูล Exchange ได้')
    }
  }, [])

  const fetchAllData = useCallback(() => {
    setLoading(true)
    Promise.all([
      fetchBanks(),
      fetchNonBanks(),
      fetchPaymentGateways(),
      fetchTelcoMobile(),
      fetchTelcoInternet(),
      fetchExchanges()
    ]).finally(() => setLoading(false))
  }, [fetchBanks, fetchNonBanks, fetchPaymentGateways, fetchTelcoMobile, fetchTelcoInternet, fetchExchanges])

  useEffect(() => {
    fetchAllData()
  }, [fetchAllData])

  const handleAdd = (dataType: string) => {
    setCurrentDataType(dataType)
    setEditingItem(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (item: MasterDataType, dataType: string) => {
    setCurrentDataType(dataType)
    setEditingItem(item)
    form.setFieldsValue({
      ...item,
      license_date: item.hasOwnProperty('license_date') && (item as Exchange).license_date
        ? dayjs((item as Exchange).license_date)
        : undefined
    })
    setModalVisible(true)
  }

  const handleDelete = async (id: number, dataType: string) => {
    try {
      let endpoint = ''
      switch (dataType) {
        case 'banks':
          endpoint = `/master-data/banks/${id}`
          break
        case 'non-banks':
          endpoint = `/master-data/non-banks/${id}`
          break
        case 'payment-gateways':
          endpoint = `/master-data/payment-gateways/${id}`
          break
        case 'telco-mobile':
          endpoint = `/master-data/telco-mobile/${id}`
          break
        case 'telco-internet':
          endpoint = `/master-data/telco-internet/${id}`
          break
        case 'exchanges':
          endpoint = `/master-data/exchanges/${id}`
          break
      }

      await api.delete(endpoint)
      message.success('ลบข้อมูลเรียบร้อยแล้ว')
      fetchAllData()
    } catch (error: any) {
      if (error.response?.status === 400) {
        message.error(error.response.data.detail || 'ไม่สามารถลบข้อมูลได้ เนื่องจากมีข้อมูลที่เชื่อมโยงอยู่')
      } else {
        message.error('ไม่สามารถลบข้อมูลได้')
      }
    }
  }

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()

      // Convert license_date to string if exists
      if (values.license_date) {
        values.license_date = dayjs(values.license_date).format('YYYY-MM-DD')
      }

      let endpoint = ''
      let method = editingItem ? 'put' : 'post'

      switch (currentDataType) {
        case 'banks':
          endpoint = editingItem
            ? `/master-data/banks/${editingItem.id}`
            : '/master-data/banks'
          break
        case 'non-banks':
          endpoint = editingItem
            ? `/master-data/non-banks/${editingItem.id}`
            : '/master-data/non-banks'
          break
        case 'payment-gateways':
          endpoint = editingItem
            ? `/master-data/payment-gateways/${editingItem.id}`
            : '/master-data/payment-gateways'
          break
        case 'telco-mobile':
          endpoint = editingItem
            ? `/master-data/telco-mobile/${editingItem.id}`
            : '/master-data/telco-mobile'
          break
        case 'telco-internet':
          endpoint = editingItem
            ? `/master-data/telco-internet/${editingItem.id}`
            : '/master-data/telco-internet'
          break
        case 'exchanges':
          endpoint = editingItem
            ? `/master-data/exchanges/${editingItem.id}`
            : '/master-data/exchanges'
          break
      }

      if (method === 'post') {
        await api.post(endpoint, values)
        message.success('เพิ่มข้อมูลเรียบร้อยแล้ว')
      } else {
        await api.put(endpoint, values)
        message.success('แก้ไขข้อมูลเรียบร้อยแล้ว')
      }

      setModalVisible(false)
      form.resetFields()
      fetchAllData()
    } catch (error: any) {
      if (error.response?.status === 400) {
        message.error(error.response.data.detail || 'ข้อมูลซ้ำกัน')
      } else {
        message.error('ไม่สามารถบันทึกข้อมูลได้')
      }
    }
  }

  const bankColumns: ColumnsType<Bank> = [
    {
      title: 'ชื่อธนาคาร',
      dataIndex: 'bank_name',
      key: 'bank_name',
      width: 250
    },
    {
      title: 'รหัส',
      dataIndex: 'bank_code',
      key: 'bank_code',
      width: 80
    },
    {
      title: 'ชื่อย่อ',
      dataIndex: 'bank_short_name',
      key: 'bank_short_name',
      width: 100
    },
    {
      title: 'ที่อยู่',
      key: 'address',
      render: (_, record) => {
        const parts = [
          record.bank_address,
          record.soi,
          record.road,
          record.district,
          record.province,
          record.postal_code
        ].filter(Boolean)
        return parts.join(' ')
      }
    },
    {
      title: 'การดำเนินการ',
      key: 'actions',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record, 'banks')}
          >
            แก้ไข
          </Button>
          <Popconfirm
            title="ยืนยันการลบข้อมูล?"
            description="คุณแน่ใจหรือไม่ว่าต้องการลบข้อมูลนี้? หากมีข้อมูลที่เชื่อมโยงอยู่จะไม่สามารถลบได้"
            onConfirm={() => handleDelete(record.id, 'banks')}
            okText="ยืนยัน"
            cancelText="ยกเลิก"
            okType="danger"
          >
            <Button
              type="link"
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
              ลบ
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  const companyColumns = (dataType: string): ColumnsType<any> => [
    {
      title: 'ชื่อบริษัท',
      dataIndex: 'company_name',
      key: 'company_name',
      width: 250
    },
    {
      title: 'ชื่อย่อ',
      dataIndex: 'company_name_short',
      key: 'company_name_short',
      width: 100
    },
    {
      title: 'เบอร์โทร',
      dataIndex: 'phone',
      key: 'phone',
      width: 120
    },
    {
      title: 'อีเมล',
      dataIndex: 'email',
      key: 'email',
      width: 180
    },
    {
      title: 'สถานะ',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (isActive: boolean) => (
        <span style={{ color: isActive ? 'green' : 'red' }}>
          {isActive ? 'ใช้งาน' : 'ปิดใช้งาน'}
        </span>
      )
    },
    {
      title: 'การดำเนินการ',
      key: 'actions',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record, dataType)}
          >
            แก้ไข
          </Button>
          <Popconfirm
            title="ยืนยันการลบข้อมูล?"
            description="คุณแน่ใจหรือไม่ว่าต้องการลบข้อมูลนี้? หากมีข้อมูลที่เชื่อมโยงอยู่จะไม่สามารถลบได้"
            onConfirm={() => handleDelete(record.id, dataType)}
            okText="ยืนยัน"
            cancelText="ยกเลิก"
            okType="danger"
          >
            <Button
              type="link"
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
              ลบ
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  const exchangeColumns: ColumnsType<Exchange> = [
    {
      title: 'ชื่อบริษัท',
      dataIndex: 'company_name',
      key: 'company_name',
      width: 250
    },
    {
      title: 'ชื่อย่อ',
      dataIndex: 'company_name_short',
      key: 'company_name_short',
      width: 100
    },
    {
      title: 'เบอร์โทร',
      dataIndex: 'phone',
      key: 'phone',
      width: 120
    },
    {
      title: 'อีเมล',
      dataIndex: 'email',
      key: 'email',
      width: 180
    },
    {
      title: 'สถานะ',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (isActive: boolean) => (
        <span style={{ color: isActive ? 'green' : 'red' }}>
          {isActive ? 'ใช้งาน' : 'ปิดใช้งาน'}
        </span>
      )
    },
    {
      title: 'การดำเนินการ',
      key: 'actions',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record, 'exchanges')}
          >
            แก้ไข
          </Button>
          <Popconfirm
            title="ยืนยันการลบข้อมูล?"
            description="คุณแน่ใจหรือไม่ว่าต้องการลบข้อมูลนี้?"
            onConfirm={() => handleDelete(record.id, 'exchanges')}
            okText="ยืนยัน"
            cancelText="ยกเลิก"
            okType="danger"
          >
            <Button
              type="link"
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
              ลบ
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  const renderFormFields = () => {
    switch (currentDataType) {
      case 'banks':
        return (
          <>
            <Form.Item name="bank_name" label="ชื่อธนาคาร" rules={[{ required: true, message: 'กรุณากรอกชื่อธนาคาร' }]}>
              <Input />
            </Form.Item>
            <Form.Item name="bank_code" label="รหัสธนาคาร">
              <Input />
            </Form.Item>
            <Form.Item name="bank_short_name" label="ชื่อย่อ">
              <Input />
            </Form.Item>
            <Form.Item name="bank_address" label="ที่อยู่">
              <TextArea rows={2} />
            </Form.Item>
            <Form.Item name="soi" label="ซอย">
              <Input />
            </Form.Item>
            <Form.Item name="moo" label="หมู่">
              <Input />
            </Form.Item>
            <Form.Item name="road" label="ถนน">
              <Input />
            </Form.Item>
            <Form.Item name="sub_district" label="แขวง/ตำบล">
              <Input />
            </Form.Item>
            <Form.Item name="district" label="เขต/อำเภอ">
              <Input />
            </Form.Item>
            <Form.Item name="province" label="จังหวัด">
              <Input />
            </Form.Item>
            <Form.Item name="postal_code" label="รหัสไปรษณีย์">
              <Input />
            </Form.Item>
          </>
        )

      case 'exchanges':
        return (
          <>
            <Form.Item name="company_name" label="ชื่อบริษัท" rules={[{ required: true, message: 'กรุณากรอกชื่อบริษัท' }]}>
              <Input />
            </Form.Item>
            <Form.Item name="company_name_short" label="ชื่อย่อ">
              <Input />
            </Form.Item>
            <Form.Item name="company_name_alt" label="ชื่อเดิม/ชื่อทางเลือก">
              <Input />
            </Form.Item>
            <Form.Item name="building_name" label="ชื่ออาคาร">
              <Input />
            </Form.Item>
            <Form.Item name="company_address" label="เลขที่">
              <Input />
            </Form.Item>
            <Form.Item name="floor" label="ชั้น">
              <Input />
            </Form.Item>
            <Form.Item name="unit" label="ห้อง/ยูนิต">
              <Input />
            </Form.Item>
            <Form.Item name="soi" label="ซอย">
              <Input />
            </Form.Item>
            <Form.Item name="moo" label="หมู่">
              <Input />
            </Form.Item>
            <Form.Item name="road" label="ถนน">
              <Input />
            </Form.Item>
            <Form.Item name="sub_district" label="แขวง/ตำบล">
              <Input />
            </Form.Item>
            <Form.Item name="district" label="เขต/อำเภอ">
              <Input />
            </Form.Item>
            <Form.Item name="province" label="จังหวัด">
              <Input />
            </Form.Item>
            <Form.Item name="postal_code" label="รหัสไปรษณีย์">
              <Input />
            </Form.Item>
            <Form.Item name="phone" label="เบอร์โทรศัพท์">
              <Input />
            </Form.Item>
            <Form.Item name="email" label="อีเมล">
              <Input type="email" />
            </Form.Item>
            <Form.Item name="website" label="เว็บไซต์">
              <Input />
            </Form.Item>
            <Form.Item name="is_active" label="สถานะ" valuePropName="checked" initialValue={true}>
              <Switch checkedChildren="ใช้งาน" unCheckedChildren="ปิดใช้งาน" />
            </Form.Item>
          </>
        )

      default:
        return (
          <>
            <Form.Item name="company_name" label="ชื่อบริษัท" rules={[{ required: true, message: 'กรุณากรอกชื่อบริษัท' }]}>
              <Input />
            </Form.Item>
            <Form.Item name="company_name_short" label="ชื่อย่อ">
              <Input />
            </Form.Item>
            {(currentDataType === 'telco-mobile' || currentDataType === 'telco-internet') && (
              <Form.Item name="building_name" label="ชื่ออาคาร">
                <Input />
              </Form.Item>
            )}
            <Form.Item name="company_address" label="ที่อยู่">
              <TextArea rows={2} />
            </Form.Item>
            <Form.Item name="soi" label="ซอย">
              <Input />
            </Form.Item>
            <Form.Item name="moo" label="หมู่">
              <Input />
            </Form.Item>
            <Form.Item name="road" label="ถนน">
              <Input />
            </Form.Item>
            <Form.Item name="sub_district" label="แขวง/ตำบล">
              <Input />
            </Form.Item>
            <Form.Item name="district" label="เขต/อำเภอ">
              <Input />
            </Form.Item>
            <Form.Item name="province" label="จังหวัด">
              <Input />
            </Form.Item>
            <Form.Item name="postal_code" label="รหัสไปรษณีย์">
              <Input />
            </Form.Item>
            <Form.Item name="phone" label="เบอร์โทรศัพท์">
              <Input />
            </Form.Item>
            <Form.Item name="email" label="อีเมล">
              <Input type="email" />
            </Form.Item>
            <Form.Item name="website" label="เว็บไซต์">
              <Input />
            </Form.Item>
            <Form.Item name="is_active" label="สถานะ" valuePropName="checked" initialValue={true}>
              <Switch checkedChildren="ใช้งาน" unCheckedChildren="ปิดใช้งาน" />
            </Form.Item>
          </>
        )
    }
  }

  const getModalTitle = () => {
    const action = editingItem ? 'แก้ไข' : 'เพิ่ม'
    switch (currentDataType) {
      case 'banks':
        return `${action}ข้อมูลธนาคาร`
      case 'non-banks':
        return `${action}ข้อมูล Non-Bank`
      case 'payment-gateways':
        return `${action}ข้อมูล Payment Gateway`
      case 'telco-mobile':
        return `${action}ข้อมูลผู้ให้บริการโทรศัพท์มือถือ`
      case 'telco-internet':
        return `${action}ข้อมูลผู้ให้บริการอินเทอร์เน็ต`
      case 'exchanges':
        return `${action}ข้อมูล Exchange`
      default:
        return `${action}ข้อมูล`
    }
  }

  const tabItems = [
    {
      key: 'banks',
      label: (
        <span>
          <BankOutlined /> ธนาคาร ({banks.length})
        </span>
      ),
      children: (
        <>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => handleAdd('banks')}
            style={{ marginBottom: 16 }}
          >
            เพิ่มธนาคาร
          </Button>
          <Table
            columns={bankColumns}
            dataSource={banks}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            scroll={{ x: 1200 }}
          />
        </>
      )
    },
    {
      key: 'non-banks',
      label: (
        <span>
          <ShopOutlined /> Non-Bank ({nonBanks.length})
        </span>
      ),
      children: (
        <>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => handleAdd('non-banks')}
            style={{ marginBottom: 16 }}
          >
            เพิ่ม Non-Bank
          </Button>
          <Table
            columns={companyColumns('non-banks')}
            dataSource={nonBanks}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            scroll={{ x: 1200 }}
          />
        </>
      )
    },
    {
      key: 'payment-gateways',
      label: (
        <span>
          <CreditCardOutlined /> Payment Gateway ({paymentGateways.length})
        </span>
      ),
      children: (
        <>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => handleAdd('payment-gateways')}
            style={{ marginBottom: 16 }}
          >
            เพิ่ม Payment Gateway
          </Button>
          <Table
            columns={companyColumns('payment-gateways')}
            dataSource={paymentGateways}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            scroll={{ x: 1200 }}
          />
        </>
      )
    },
    {
      key: 'telco-mobile',
      label: (
        <span>
          <MobileOutlined /> Telco Mobile ({telcoMobile.length})
        </span>
      ),
      children: (
        <>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => handleAdd('telco-mobile')}
            style={{ marginBottom: 16 }}
          >
            เพิ่มผู้ให้บริการโทรศัพท์มือถือ
          </Button>
          <Table
            columns={companyColumns('telco-mobile')}
            dataSource={telcoMobile}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            scroll={{ x: 1200 }}
          />
        </>
      )
    },
    {
      key: 'telco-internet',
      label: (
        <span>
          <GlobalOutlined /> Telco Internet ({telcoInternet.length})
        </span>
      ),
      children: (
        <>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => handleAdd('telco-internet')}
            style={{ marginBottom: 16 }}
          >
            เพิ่มผู้ให้บริการอินเทอร์เน็ต
          </Button>
          <Table
            columns={companyColumns('telco-internet')}
            dataSource={telcoInternet}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            scroll={{ x: 1200 }}
          />
        </>
      )
    },
    {
      key: 'exchanges',
      label: (
        <span>
          <SwapOutlined /> Crypto Exchange ({exchanges.length})
        </span>
      ),
      children: (
        <>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => handleAdd('exchanges')}
            style={{ marginBottom: 16 }}
          >
            เพิ่ม Exchange
          </Button>
          <Table
            columns={exchangeColumns}
            dataSource={exchanges}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            scroll={{ x: 1200 }}
          />
        </>
      )
    }
  ]

  return (
    <div style={{ padding: '20px' }}>
      <Title level={2}>จัดการข้อมูล Master Data</Title>

      <Card>
        <Tabs items={tabItems} />
      </Card>

      <Modal
        title={getModalTitle()}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => {
          setModalVisible(false)
          form.resetFields()
        }}
        width={700}
        okText="บันทึก"
        cancelText="ยกเลิก"
      >
        <Form
          form={form}
          layout="vertical"
        >
          {renderFormFields()}
        </Form>
      </Modal>
    </div>
  )
}
