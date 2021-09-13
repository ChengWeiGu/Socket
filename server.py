import socket
import json
import datetime
import random
import xml.etree.ElementTree as ET



def generate_json_data(filename):
    
    json_data = {}
    tree = ET.parse(filename)
    # tree = ET.fromstring(xml_string)
    root = tree.getroot() # root: <Panel></Panel>
    
    # print(root.attrib) # root's attribs
    print("the product model is: %s" % root.get("cModel"))
    print("the number of multi-boards is: %d" % len(root))
    
    
    json_data['station_id'] = root.get('StationId') #機台名稱
    json_data['test_start_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') #檢測時間
    json_data['ModelName'] = "" # 機台型號
    json_data['sn'] = root[0].get("BoardSN") #板子條碼: 所有聯版都相同
    json_data['status'] = root.get('Status') #大板狀態
    
    
    json_data['keys'] = []
    for board in root:
        for component in board:
            # print(component.tag, component.attrib) # list the tag name and its attribs
            json_data['keys'] += [{
                                    'key_name': component.get('CompName'),
                                    'box_name': "",
                                    'ai_result': "OK" if random.random() <= 0.5 else "NG",
                                    'ai_type': ""
                                                                        }]
    
    
    # print(json_data)
    return json_data



def main_server():
    bind_ip = '127.0.0.1'
    bind_port = 8000
    
    server_run_enable = True
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP宣告
    # server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP宣告

    server.bind((bind_ip,bind_port))
    server.listen(3)
    print("[*] Listening on %s:%d " % (bind_ip,bind_port))

    while server_run_enable:
        client,addr = server.accept()
        print('Connected by ', addr)

        while True:
            print("="*80)
            filename = client.recv(6144)
            filename = filename.decode('utf-8') #bytes to string
            print("recv: %s " % (filename))
            
            # close the server
            if filename == 'shutdown' or filename == 'sd':
                print('close the server')
                server.close()
                server_run_enable = False
                break
            # return json data from inputting xml
            elif filename.endswith('.xml'):
                try:
                    json_data = generate_json_data(filename)
                except:
                    json_data = {}
                json_data = json.dumps(json_data)
                client.send(json_data.encode())
            # otherwise, send error info to client
            else:
                print("get error filename. xml required!")
                client.send("ERROR: got unexpected filename(not xml)".encode())



if __name__ == "__main__":
    main_server()
    