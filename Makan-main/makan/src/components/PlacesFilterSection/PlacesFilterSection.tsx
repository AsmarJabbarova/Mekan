import { Radio, Select, Slider } from 'antd';
import {StarFilled, StarOutlined} from '@ant-design/icons';
import './PlacesFilterSection.css';
import { FaSearch } from 'react-icons/fa';

const handleChange = (value: string) => {
  console.log(`selected ${value}`);
};

const PlacesFilterSection: React.FC = () => {
    return (
      <div className="side-filter-sec">
        <Select
          size='large'
          variant='filled'
          showSearch
          placeholder="Locations"
          style={{ width: '100%' }}
          onChange={handleChange}
          filterOption={(input, option) =>
            (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
          }
          options={[
            { value: '1', label: 'Jack' },
            { value: '2', label: 'Lucy' },
            { value: '3', label: 'Tom' },
          ]}
        />
        <Select
          showSearch
          variant='filled'
          size='large'
          placeholder="Adventure Type"
          style={{ width: '100%' }}
          onChange={handleChange}
          filterOption={(input, option) =>
            (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
          }
          options={[
            { value: '1', label: 'Jack' },
            { value: '2', label: 'Lucy' },
            { value: '3', label: 'Tom' },
          ]}
        />

        <Slider style={{ width: '80%' }} id='range' range defaultValue={[0, 50000]} max={50000} />
        <div >
        <Radio.Group className='filter-rate-sec'>
          <Radio value={1}>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
          </Radio>
          <Radio value={2}>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
          </Radio>
          <Radio value={3}>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
          </Radio>
          <Radio value={4}>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarOutlined style={{ color: '#F7931E' }}/>
          </Radio>
          <Radio value={5}>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
            <StarFilled style={{ color: '#F7931E' }}/>
          </Radio>
        </Radio.Group>
        </div>
        <button type="submit" className="submit-button">
              <FaSearch/> Search
            </button>
      </div>
    );
  }
  
  export default PlacesFilterSection;