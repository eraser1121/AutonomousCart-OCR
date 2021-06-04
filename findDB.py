def find_name(text) :
    if text.find('지우')>0 or text.find('최지우')>0 or text.find('최지')>0 :
        return '최지우'
    else if text.find('길동')>0 or text.find('홍길동')>0 or text.find('홍길')>0 :
        return '홍길동'
    else if text.find('대한')>0 or text.find('강대한')>0 or text.find('강대')>0 :
        return '강대한'
    else if text.find('민국')>0 or text.find('박민국')>0 or text.find('박민')>0 :
        return '박민국'
    else :
        return 'error : name 데이터가 존재하지 않음' 

def find_address(text) :
    if text.find('902')>0 :
        return '최지우'
    else if text.find('801')>0 :
        return '홍길동'
    else if text.find('803')>0  :
        return '강대한'
    else if text.find('702')>0 :
        return '박민국'
    else :
        return 'error : address 데이터가 존재하지 않음'

def set_destination(name, address):
    if name == '최지우' or address == '최지우' :
        return 902
    else if name == '홍길동' or address == '홍길동' :
        return 801
    else if name == '강대한' or address == '강대한' :
        return 803
    else if name == '박민국' or address == '박민국' :
        return 702
    else :
        return 'error : no destination"
 
