#encoding: utf-8
import sys
import os
from Constant import *
import  logging
# logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%H:%M:%S'
#                 )


error=[]
tempchar=[]
def tape_reader(line,current_state,index,line_num):
    logging.info("tape reader called :parameter:line:"+str(line)+"   current_state:"+str(current_state)+"     index:"+str(index)+"     line_num:"+str(line_num))
    index+=1
    if index==len(line):
        logging.info("到达行尾")
        # end of line
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
        if ch in SINGLE_DELIMITER:
            print(ch+" 单界符 line:"+str(line_num))
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
    if current_state ==STATE_SIGN:
        if line[index-1] in ['>','<','!'] and line[index]=='=':
            print(str(line[line-1:line+1])+" 双界符 "+str(line_num))
            tempchar.clear()
        else:
            error.append("error in line" +line_num+", "+str(line[index]))
        return STATE_START






def change_id_state(line,index,line_num,current_state):
    logging.info("change_id_state called    line:"+str(line).strip()+"  index:"+str(index)+"    line_num:"+str(line_num))
    if line[index].isalnum() or line[index]=='_':
        tempchar.append(line[index])
        return STATE_ID_1
    elif line[index].isspace():
        if ''.join(tempchar).strip() in KEYWORD:
            print(''.join(tempchar)+" keyword "+" line:"+str(line_num))
        else:
            print(''.join(tempchar)+" id "+" line:"+str(line_num))
        tempchar.clear()
        return refresh(line[index],line_num)
    else:
        return refresh(line[index],line_num)


def change_literal_state(line,index,line_num,current_state):
    logging.info("change_literal_state called    line:"+str(line)+"  index:"+str(index)+"    line_num:"+str(line_num))

    ch=line[index]
    if current_state==STATE_LITERAL_1:
        if ch!="\\" and ch!="\"":
            tempchar.append(ch)
            return STATE_LITERAL_1
        if ch=="\\":
            tempchar.append('\\')
            return STATE_LITERAL_2
        if ch=='"':
            tempchar.append('"')
            print(''.join(tempchar)+" literal line:"+str(line_num))
            tempchar.clear()
            return STATE_LITERAL_3
    if current_state==STATE_LITERAL_2:
        if ch.isalnum():
            tempchar.append(ch)
            return  STATE_LITERAL_1
        else:
            print("error in line"+str(line_num)+" \\后面的非法字符")
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
            print(''.join(tempchar)+" literal line:"+str(line_num))
            tempchar.clear()
            return STATE_LITERAL_3
    if current_state==STATE_LITERAL_2:
        if ch.isalnum():
            tempchar.append(ch)
            return  STATE_LITERAL_1
        else:
            print("error in line"+str(line_num)+" \\后面的非法字符")
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
        else:
            tempchar.append(ch)
            print(''.join(tempchar)+"   数字  line: "+str(line_num))
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
            print(''.join(tempchar)+"   数字  line: "+str(line_num))
            return refresh(ch,line_num)
    if current_state==STATE_DIGIT_3:
        if ch.isdigit():
            tempchar.append(ch)
            return STATE_DIGIT_3
        else:
            tempchar.append(ch)
            print(''.join(tempchar)+"   数字  line: "+str(line_num))
            return refresh(ch,line_num)


def change_note_state(line,index,line_num,current_state):
    logging.info("change_note_state called    line:"+str(line)+"  index:"+str(index)+"    line_num:"+str(line_num))

    ch=line[index]
    if current_state==STATE_NOTE_1:
        if ch=='*':
            tempchar.append('*')
            return STATE_NOTE_2
        else:
            print("/ 除号 line:"+str(line_num))
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
            print("error 注释格式错误，line："+str(line_num))
            return STATE_END
    if current_state==STATE_NOTE_4:
        tempchar.append(ch)
        print(''.join(tempchar)+" 注释 line："+str(line_num))
        refresh(ch,line_num)



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
    if ch in SINGLE_DELIMITER:
        print(ch+"  singlequote line:" + str(line_num))
        tempchar.clear()
        return STATE_START
    if ch.isspace():
        tempchar.clear()
        return STATE_START
def main():

    # file_name=sys.argv[1]
    file=open("/Users/user/Desktop/a.c", mode="r")
    file_content=file.readlines()
    file_lines=len(file_content)
    print(file_content)
    line_num=0
    for line in file_content:
        index=-1
        line_num+=1
        current_state=STATE_START
        while index!=len(line):
            current_state=tape_reader(line,current_state,index,line_num)
            index+=1



if __name__=="__main__":
    main()