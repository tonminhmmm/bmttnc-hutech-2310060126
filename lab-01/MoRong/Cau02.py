
import re

def tinh_tong_so_nguyen(s):

    ds_str = re.findall(r'-?\d+', s)
    
    tong_duong = 0
    tong_am    = 0
    for num_str in ds_str:
        val = int(num_str)
        if val >= 0:
            tong_duong += val
        else:
            tong_am    += val
            tong_duong += abs(val)  
    return tong_duong, tong_am

if __name__ == "__main__":
    chuoi = "-100#^sdfkj8902w3ir021@swf-20"
    tong_duong, tong_am = tinh_tong_so_nguyen(chuoi)
    
    print("Chuỗi đầu vào:", chuoi)
    print(f"Giá trị dương: {tong_duong}")  
    print(f"Giá trị âm:   {tong_am}")     
