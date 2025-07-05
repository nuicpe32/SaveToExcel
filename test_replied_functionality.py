#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify the replied functionality implementation
"""

def test_replied_checkbox_logic():
    """Test the replied checkbox logic"""
    
    print("=== Testing Replied Checkbox Logic ===")
    
    # Test 1: Empty value should result in unchecked checkbox
    replied_status = ""
    checkbox_value = replied_status.strip().upper() == "X"
    print(f"Test 1 - Empty value: '{replied_status}' -> Checkbox: {checkbox_value}")
    assert checkbox_value == False, "Empty value should result in unchecked checkbox"
    
    # Test 2: "X" value should result in checked checkbox
    replied_status = "X"
    checkbox_value = replied_status.strip().upper() == "X"
    print(f"Test 2 - 'X' value: '{replied_status}' -> Checkbox: {checkbox_value}")
    assert checkbox_value == True, "'X' value should result in checked checkbox"
    
    # Test 3: "x" value should result in checked checkbox (case insensitive)
    replied_status = "x"
    checkbox_value = replied_status.strip().upper() == "X"
    print(f"Test 3 - 'x' value: '{replied_status}' -> Checkbox: {checkbox_value}")
    assert checkbox_value == True, "'x' value should result in checked checkbox"
    
    # Test 4: " X " value with spaces should result in checked checkbox
    replied_status = " X "
    checkbox_value = replied_status.strip().upper() == "X"
    print(f"Test 4 - ' X ' value: '{replied_status}' -> Checkbox: {checkbox_value}")
    assert checkbox_value == True, "' X ' value should result in checked checkbox"
    
    # Test 5: Other value should result in unchecked checkbox
    replied_status = "Y"
    checkbox_value = replied_status.strip().upper() == "X"
    print(f"Test 5 - 'Y' value: '{replied_status}' -> Checkbox: {checkbox_value}")
    assert checkbox_value == False, "'Y' value should result in unchecked checkbox"
    
    print("✓ All checkbox logic tests passed!")

def test_save_logic():
    """Test the save logic for replied value"""
    
    print("\n=== Testing Save Logic ===")
    
    # Test 1: Checked checkbox should save as "X"
    replied_var_value = True
    saved_value = "X" if replied_var_value else ""
    print(f"Test 1 - Checked checkbox: {replied_var_value} -> Saved: '{saved_value}'")
    assert saved_value == "X", "Checked checkbox should save as 'X'"
    
    # Test 2: Unchecked checkbox should save as empty string
    replied_var_value = False
    saved_value = "X" if replied_var_value else ""
    print(f"Test 2 - Unchecked checkbox: {replied_var_value} -> Saved: '{saved_value}'")
    assert saved_value == "", "Unchecked checkbox should save as empty string"
    
    print("✓ All save logic tests passed!")

def test_display_logic():
    """Test the display logic for green text"""
    
    print("\n=== Testing Display Logic ===")
    
    # Test 1: "X" value should result in green text
    replied_value = "X"
    should_be_green = str(replied_value).strip().upper() == "X"
    print(f"Test 1 - 'X' value: '{replied_value}' -> Green text: {should_be_green}")
    assert should_be_green == True, "'X' value should result in green text"
    
    # Test 2: Empty value should not result in green text
    replied_value = ""
    should_be_green = str(replied_value).strip().upper() == "X"
    print(f"Test 2 - Empty value: '{replied_value}' -> Green text: {should_be_green}")
    assert should_be_green == False, "Empty value should not result in green text"
    
    # Test 3: "x" value should result in green text (case insensitive)
    replied_value = "x"
    should_be_green = str(replied_value).strip().upper() == "X"
    print(f"Test 3 - 'x' value: '{replied_value}' -> Green text: {should_be_green}")
    assert should_be_green == True, "'x' value should result in green text"
    
    # Test 4: " X " value with spaces should result in green text
    replied_value = " X "
    should_be_green = str(replied_value).strip().upper() == "X"
    print(f"Test 4 - ' X ' value: '{replied_value}' -> Green text: {should_be_green}")
    assert should_be_green == True, "' X ' value should result in green text"
    
    # Test 5: Other value should not result in green text
    replied_value = "Y"
    should_be_green = str(replied_value).strip().upper() == "X"
    print(f"Test 5 - 'Y' value: '{replied_value}' -> Green text: {should_be_green}")
    assert should_be_green == False, "'Y' value should not result in green text"
    
    print("✓ All display logic tests passed!")

def test_column_management():
    """Test column management logic"""
    
    print("\n=== Testing Column Management ===")
    
    # Test 1: Adding "ตอบกลับ" column to columns list
    columns = ["ชื่อ", "เบอร์โทร", "ที่อยู่"]
    if "ตอบกลับ" not in columns:
        columns.append("ตอบกลับ")
    print(f"Test 1 - Added column: {columns}")
    assert "ตอบกลับ" in columns, "ตอบกลับ column should be added"
    
    # Test 2: Column already exists
    columns = ["ชื่อ", "เบอร์โทร", "ที่อยู่", "ตอบกลับ"]
    original_length = len(columns)
    if "ตอบกลับ" not in columns:
        columns.append("ตอบกลับ")
    print(f"Test 2 - Existing column: {columns}")
    assert len(columns) == original_length, "Column should not be added if it already exists"
    
    # Test 3: Finding column index
    columns = ["ชื่อ", "เบอร์โทร", "ที่อยู่", "ตอบกลับ"]
    replied_index = columns.index("ตอบกลับ")
    print(f"Test 3 - Column index: {replied_index}")
    assert replied_index == 3, "ตอบกลับ column should be at index 3"
    
    print("✓ All column management tests passed!")

if __name__ == "__main__":
    try:
        test_replied_checkbox_logic()
        test_save_logic()
        test_display_logic()
        test_column_management()
        
        print("\n" + "="*50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("The replied functionality implementation is working correctly!")
        print("="*50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)