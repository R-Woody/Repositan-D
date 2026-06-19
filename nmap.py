import xml.etree.ElementTree as ET
import sys

xml_file = 'scan_result.xml'

try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except FileNotFoundError:
    print(f"[エラー] {xml_file} が見つかりません。")
    sys.exit(1)

# 第1階層（親ノード）
print("L2スイッチ (192.168.10.0/24)")

for host in root.findall('host'):
    ip_elem = host.find("./address[@addrtype='ipv4']")
    if ip_elem is None: continue
    ip = ip_elem.get('addr')
    
    os_name = "OS不明"
    os_match = host.find("./os/osmatch")
    if os_match is not None:
        os_name = os_match.get('name').split('(')[0].strip()
        
    # 第2階層（ホスト情報）：タブ1つ
    print(f"\t{ip} [{os_name}]")
    
    # 開いているポートを個別にループ処理
    has_open_port = False
    for port in host.findall("./ports/port"):
        state = port.find('state').get('state')
        if state == 'open':
            has_open_port = True
            port_id = port.get('portid')
            service = port.find('service').get('name') if port.find('service') is not None else "unk"
            
            # 第3階層（ポート情報）：【最重要】タブを2つにする(\t\t)
            print(f"\t\tPort: {port_id}/{service}")
            
    if not has_open_port:
        # ポートが開いていない場合も、下の階層に「なし」をぶら下げる
        print("\t\tPort: なし")