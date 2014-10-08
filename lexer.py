# #!/usr/bin/python3
# import Constant
# import sys
# import os
# SYMBOL=[]
#
# def main():
#     result=[]
#     file_name=sys.argv[1]
#     file=open(file_name, mode="r",encoding='utf8')
#     file_content=file.readlines()
#     file_lines=len(file_content)
#     line_num=0
#     for line in file_content:
#         line_num+=1
#         tape_reader(line.strip(),line_num,0)
#
#
# def tape_reader(line,line_num,start_index):
#
#     result=[]
#     temp_index=start_index
#     if line[start_index:].isspace():
#         # 整行为空
#         return result.append({"word":None,"class":None,"line_num":line_num,"note":"空行"})
#
#     if is_note(line,line_num,start_index):
#         # 遇到注释
#         return result.append({"word":None,"class":"NOTE","line_num":line_num,"note":"注释"})
#     if line[start_index].isalpha():
#         temp_index+=1
#         while(line[temp_index].isalnum() ):
#             temp_index+=1
#             if len(line)==start_index:
#                 ID=line[start_index:temp_index]
#                 if ID in Constant.KEYWORD:
#                     result+={"word":ID,"class":"keyword","line_num":line_num,"note":"keyword"}
#
#                 else:
#                     result+={"word":ID,"class":"ID","line_num":line_num,"note":"标示符"}
#                 return result
#
#
#
#         # 遇到空格等
#         if line[temp_index].isspace():
#             ID=line[start_index:temp_index]
#             if ID in Constant.KEYWORD:
#                 result+={"word":ID,"class":"keyword","line_num":line_num,"note":"keyword"}
#             else:
#                 result+={"word":ID,"class":"ID","line_num":line_num,"note":"标示符"}
#         if is_note(line,line_num,temp_index):
#                     return result.append({"word":None,"class":"NOTE","line_num":line_num,"note":"注释"})
#
#
#
#
#
#
#
#
#
#
# def is_note(line,line_num,start_index):
#     if line[start_index:].startswith(r'//') or line[start_index:].startswith(r'/*')
#
#
#
#
#
#
#
#
#
# if __name__=="__main__":
#     main()
#
#
