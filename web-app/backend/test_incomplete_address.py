#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for police station with incomplete address
"""

import requests
import json

def test_incomplete_address():
    """Test with address that should find stations with incomplete addresses"""
    
    # ทดสอบกับที่อยู่ที่ควรจะเจอสถานีที่ไม่มีเลขที่
    test_address = "บ้านเลขที่ 123 ตำบล ศรีสงคราม อำเภอ วังสะพุง จังหวัด เลย"
    
    try:
        response = requests.post('http://localhost:8000/api/v1/police-stations/search', 
                               json={'address': test_address},
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            print('=== ผลการทดสอบ (สถานีที่ไม่มีเลขที่) ===')
            print(f'มีสถานีที่ตรงตำบล: {data.get("exact_match") is not None}')
            print(f'มีสถานีในอำเภอ: {len(data.get("district_matches", []))}')
            print(f'มีสถานีในจังหวัด: {len(data.get("province_matches", []))}')
            print(f'มีข้อมูลไม่สมบูรณ์: {data.get("has_incomplete_address", False)}')
            print(f'ข้อความแจ้งเตือน: {data.get("warning_message", "ไม่มี")}')
            
            # แสดงสถานีทั้งหมดที่พบ
            all_stations = []
            if data.get('exact_match'):
                all_stations.append(data['exact_match'])
            all_stations.extend(data.get('district_matches', []))
            all_stations.extend(data.get('province_matches', []))
            
            print(f'\n=== สถานีทั้งหมดที่พบ ({len(all_stations)} แห่ง) ===')
            for i, station in enumerate(all_stations[:10], 1):  # แสดงแค่ 10 แห่งแรก
                print(f'{i}. {station["station_name"]}')
                print(f'   ที่อยู่: {station["address"]}')
                # ตรวจสอบว่าที่อยู่มีเลขที่หรือไม่
                has_number = station["address"] and station["address"].strip().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
                print(f'   มีเลขที่: {"ใช่" if has_number else "ไม่"}')
                print()
                
        else:
            print(f'Error: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    test_incomplete_address()
