#encoding: utf-8
import sys
import os
from Constant import *
import  logging
# logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%H:%M:%S'
#                 )
ID=[]
keyword=[]
error=[]
tempchar=[]
result=[]
def tape_reader(line,current_state,index,line_num):
    logging.info("tape reader called :parameter:line:"+str(line)+"   current_state:"+str(current_state)+"     index:"+str(index)+"     line_num:"+str(line_num))
    index+=1
    if index==len(line):
        logging.info("到达行尾")
        # end of line
        if len(tempchar)>0:
            error.append({"description":''.join(tempchar)+"错误，到达行尾前未结束","line":line_num})
        tempchar.clear()
        return STATE_START
    logging.info("tape reader is reading character :"+line[index])

    if current_state==STATE_START :
        logging.info("分配起始状态")
        ch=line[index]
        tempchar.append(ch)

        if ch.isalpha()or ch=="_":
            return STATE_ID_1
        if ch=="/":

            return STATE_NOTE_1
        if ch=="\"":
            return STATE_LITERAL_1
        if ch=='0':
            return STATE_DIGIT_1
        if ch.isdigit():
            return STATE_DIGIT_2
        if ch=="'":
            return STATE_SINGLEQUOTE_1
        if ch in SIGN:
            if ch in DOUBLE_DELIMITER_FIRST:
                if ch in ['>','<','!']:
                    return STATE_SIGN_2
                if ch in ['+','-']:
                    return STATE_SIGN_3
            else:
                # 单界符，可以直接输出
                #print(ch+" 单界符 line:"+str(line_num))
                result.append({"token":ch,"description":"单界符","line":line_num})
                tempchar.clear()
                return STATE_START
        if ch.isspace():
            tempchar.clear()
            return STATE_START




    if current_state in GROUP_ID:
        return change_id_state(line,index,line_num,current_state)
    if current_state in GROUP_LITERAL:
        return change_literal_state(line,index,line_num,current_state)
    if current_state in GROUP_NOTE:
        return change_note_state(line,index,line_num,current_state)
    if current_state in GROUP_SINGLEQUOTE:
        return change_singlequote_state(line,index,line_num,current_state)
    if current_state in GROUP_DIGIT:
        return change_digit_state(line,index,line_num,current_state)
    if current_state in GROUP_SIGN:
        if current_state==STATE_SIGN_1:
            logging.warn("should not be here")
        else:
            return change_sign_state(line ,index,line_num,current_state)
        # if line[index-1] in ['>','<','!'] and line[index]=='=':
        #     result.append({"token":line[line-1:line+1],"description":"双界符","line":line_num})
        #     #print(str(line[line-1:line+1])+" 双界符 "+str(line_num))
        #     tempchar.clear()
        # else:
        #     error.append("error in line" +line_num+", "+str(line[index]))
        # return STATE_START






def change_id_state(line,index,line_num,current_state):
    logging.info("change_id_state called    line:"+str(line).strip()+"  index:"+str(index)+"    line_num:"+str(line_num))
    if line[index].isalnum() or line[index]=='_':
        tempchar.append(line[index])
        return STATE_ID_1
    elif line[index].isspace():
        if ''.join(tempchar).strip() in KEYWORD:
            result.append({"token":''.join(tempchar),"description":"关键字","line":line_num})
            r=True
            for k  in keyword:
                if k["token"]==''.join(tempchar):
                    r=False
                    break
            if r==True:
                keyword.append({"token":''.join(tempchar),"description":"关键字","line":line_num})

            #print(''.join(tempchar)+" keyword "+" line:"+str(line_num))
        else:
            result.append({"token":''.join(tempchar),"description":"ID","line":line_num})
            r=True
            for k  in ID:
                if k["token"]==''.join(tempchar):
                    r=False
                    break
            if r==True:
                ID.append({"token":''.join(tempchar),"description":"ID","line":line_num})

            #print(''.join(tempchar)+" id "+" line:"+str(line_num))
        tempchar.clear()
        return refresh(line[index],line_num)
    else:
        return refresh(line[index],line_num)


def change_literal_state(line,index,line_num,current_state):
    logging.info("change_literal_state called    line:"+str(line)+"  index:"+str(index)+"    line_num:"+str(line_num))

    ch=line[index]
    if current_state==STATE_LITERAL_1:
        if ch!="\"":
            tempchar.append(ch)
            return STATE_LITERAL_1
        # if ch=="\\":
        #     tempchar.append('\\')
            # return STATE_LITERAL_2
        if ch=='"':
            tempchar.append('"')
            result.append({"token":''.join(tempchar),"description":"双引号字符串","line":line_num})

            #print(''.join(tempchar)+" literal line:"+str(line_num))
            tempchar.clear()
            return STATE_LITERAL_3
        # 非法字符
        error.append({"description":''.join(tempchar)+"字符串非法，不已双引号作为结尾","line":line_num})
        tempchar.clear()

        return STATE_START
    if current_state==STATE_LITERAL_2:
        if ch.isalnum():
            tempchar.append(ch)
            return  STATE_LITERAL_1
        else:
            error.append({"description":"\\后面的非法字符"})
            #print("error in line"+str(line_num)+" \\后面的非法字符")
            tempchar.clear()
            return STATE_START
    if current_state==STATE_LITERAL_3:
        return refresh(line[index],line_num)





def change_singlequote_state(line,index,line_num,current_state):
    logging.info("change_singlequote_state called    line:"+str(line)+"  index:"+str(index)+"    line_num:"+str(line_num))

    ch=line[index]
    if current_state==STATE_LITERAL_1:
        if ch!="\\" and ch!="\'":
            tempchar.append(ch)
            return STATE_LITERAL_1
        if ch=="\\":
            tempchar.append('\\')
            return STATE_LITERAL_2
        if ch=="'":
            tempchar.append("'")
            result.append({"token":''.join(tempchar),"description":"单引号字符串","line":line_num})

            #print(''.join(tempchar)+" literal line:"+str(line_num))
            tempchar.clear()
            return STATE_LITERAL_3
    if current_state==STATE_LITERAL_2:
        if ch.isalnum():
            tempchar.append(ch)
            return  STATE_LITERAL_1
        else:
            error.append({"description":"error in line"+str(line_num)+" \\后面的非法字符","line":line_num})
            #print("error in line"+str(line_num)+" \\后面的非法字符")
            tempchar.clear()
            return STATE_END
    if current_state==STATE_SINGLEQUOTE_3:
       return refresh(line[index],line_num)



def change_digit_state(line,index,line_num,current_state):
    logging.info("change_digit_state called    line:"+str(line)+"  index:"+str(index)+"    line_num:"+str(line_num))

    ch=line[index]
    if current_state==STATE_DIGIT_1:
        if ch.isdigit():
            tempchar.append(ch)
            return STATE_DIGIT_1
        if ch=='.':
            tempchar.append(ch)
            return STATE_DIGIT_3
        if ch.isspace():
            tempchar.append(ch)
            result.append({"token":''.join(tempchar),"description":"十进制数字或小数","line":line_num})

            #print(''.join(tempchar)+"   数字  line: "+str(line_num))
            return refresh(ch,line_num)
        else:
            tempchar.append(ch)
            error.append({"description":''.join(tempchar)+"十进制数字或小数格式错误","line":line_num})
            tempchar.clear()
            return refresh(ch ,line_num)
            

            # #print(''.join(tempchar)+"   数字  line: "+str(line_num))
            return refresh(ch,line_num)
    if current_state==STATE_DIGIT_2:
        if ch.isdigit():
            tempchar.append(ch)
            return STATE_DIGIT_2
        if ch=='.':
            tempchar.append(ch)
            return STATE_DIGIT_3
        else:
            # tempchar.append(ch)
            result.append({"token":''.join(tempchar),"description":"十进制数字或小数","line":line_num})

            #print(''.join(tempchar)+"   数字  line: "+str(line_num))
            return refresh(ch,line_num)
    if current_state==STATE_DIGIT_3:
        if ch.isdigit():
            tempchar.append(ch)
            return STATE_DIGIT_3
        else:
            tempchar.append(ch)
            result.append({"token":''.join(tempchar),"description":"十进制数字或小数","line":line_num})

            #print(''.join(tempchar)+"   数字  line: "+str(line_num))
            return refresh(ch,line_num)


def change_note_state(line,index,line_num,current_state):
    logging.info("change_note_state called    line:"+str(line)+"  index:"+str(index)+"    line_num:"+str(line_num))

    ch=line[index]
    if current_state==STATE_NOTE_1:
        if ch=='*':
            tempchar.append('*')
            return STATE_NOTE_2
        else:
            result.append({"token":"/","description":"除号","line":line_num})
            #print("/ 除号 line:"+str(line_num))
            return refresh(ch,line_num)
    if current_state==STATE_NOTE_2:
        if ch!='*':
            tempchar.append(ch)
            return STATE_NOTE_2
        else:
            tempchar.append(ch)
            return STATE_NOTE_3
    if current_state==STATE_NOTE_3:
        if ch=='/':
            tempchar.append(ch)

            return STATE_NOTE_4
        else:
            error.append({"description":"error 注释格式错误","line":line_num})
            #print("error 注释格式错误，line："+str(line_num))
            return STATE_END
    if current_state==STATE_NOTE_4:
        tempchar.append(ch)
        result.append({"token":''.join(tempchar),"description":"注释","line":line_num})

        #print(''.join(tempchar)+" 注释 line："+str(line_num))
        refresh(ch,line_num)

def change_sign_state(line ,index,line_num,current_state):
    # if current_state==STATE_SIGN_1:
    #     result.append({"token":''.join(tempchar),"description":"注释","line":line_num})
    ch=line[index]
    if current_state==STATE_SIGN_2:
        if ch=="=":
            tempchar.append("=")
            result.append({"token":''.join(tempchar),"description":"双界符>=或<=或!=","line":line_num})
            tempchar.clear()
            return STATE_SIGN_4
        else:
            result.append({"token":''.join(tempchar),"description":"单界符>或<","line":line_num})
            tempchar.clear()
            return refresh(ch,line_num)

    if current_state==STATE_SIGN_3:
        if (ch=="+"and line[index-1]=='+')or (ch=="-"and line[index-1]=='-'):
            tempchar.append(ch)
            result.append({"token":''.join(tempchar),"description":"双界符++或--","line":line_num})
            tempchar.clear()
            return STATE_SIGN_5
        else:
            result.append({"token":''.join(tempchar),"description":"单界符+或-","line":line_num})
            tempchar.clear()
            return refresh(ch,line_num)
    if current_state==STATE_SIGN_4 or current_state==STATE_SIGN_5:
        return refresh(ch,line_num)


def refresh(ch, line_num):
    logging.info("refresh called    ch:"+str(ch)+"    line_num:"+str(line_num))
    tempchar.clear()
    tempchar.append(ch)
    current_state = STATE_START
    if ch.isalpha():
        return STATE_ID_1
    if ch == "/":
        return STATE_NOTE_1
    if ch == "\"":
        return STATE_LITERAL_1
    if ch == '0':
        return STATE_DIGIT_1
    if ch.isdigit():
        return STATE_DIGIT_2
    if ch == "'":
        return STATE_SINGLEQUOTE_1
    # if ch in SINGLE_DELIMITER:
    #     result.append({"token":ch,"description":"单界符","line":line_num})
    #
    #     #print(ch+"  singlequote line:" + str(line_num))
    #     tempchar.clear()
    #     return STATE_START
    if ch in SIGN:
            if ch in DOUBLE_DELIMITER_FIRST:
                if ch in ['>','<','!']:
                    return STATE_SIGN_2
                if ch in ['+','-']:
                    return STATE_SIGN_3
            else:
                # 单界符，可以直接输出
                #print(ch+" 单界符 line:"+str(line_num))
                result.append({"token":ch,"description":"单界符","line":line_num})
                tempchar.clear()
                return STATE_START
    if ch.isspace():
        tempchar.clear()
        return STATE_START
def main():
    SIGN=SINGLE_DELIMITER.extend(DOUBLE_DELIMITER_FIRST)
    file_name=sys.argv[1]
    file=open(file_name, mode="r")
    file_content=file.readlines()
    line_num=0
    for line in file_content:
        index=-1
        line_num+=1
        current_state=STATE_START
        while index!=len(line):
            current_state=tape_reader(line,current_state,index,line_num)
            index+=1
    for r in result:
        print('{0:9}'.format(r['token'])+'{0:^30}'.format(r['description'])+'{0:^1}'.format(r['line']))

    print("===================error====================")
    for e in error:
        print(e)
    # print(error)

    print("===================ID====================")
    for i in ID:
        print(i)
    print("===================keyword====================")
    for k in keyword:
        print(k)



if __name__=="__main__":
    main()