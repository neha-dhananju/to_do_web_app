from flask import Flask , render_template,request,redirect,url_for
import os

app=Flask(__name__)
@app.route('/load_task')
def load_task(filename):
    try:
        with open(filename,'r') as file:
            content =file.readlines()
            print("Current Tasks : ")
            for i,task in enumerate(content,start=1):
                print(f'{i} : {task}')
            done=input("\nEnter the task numbers you've completed ,(e.g : 2,3) : ")
            if done.strip()=="":
                print("None \n")
                with open(filename, 'a') as file:
                    while True:
                        user_inp=input("Press enter Twice if there are no tasks to write")
                        if user_inp.strip()=="":
                            break
                        file.write(user_inp+'\n')
                exit
            else:
                done_list=done.strip().split(',')

                done_index=[int(i)-1 for i in done_list]

                remaining=[task for i,task in enumerate(content) if i not in done_index]

                if remaining is not None:
                    print("Remaining Task\n")
                    for i,task in enumerate(remaining,start=1):
                        print(f'{i} : {task}')
                else:
                    print("No task remaining")
            
                with open(filename, 'w') as file:
                    for task in remaining:
                        file.write(task)
            


    except FileNotFoundError:
        pass




@app.route('/write_tasks')
def write_tasks(filename):
    try:
        file_exists=os.path.exists(filename)
        mode='a' if file_exists else 'w'
        with open(filename,mode) as in_file:
            while True:
                user_input=input()
                if user_input.strip()=="":   # empty input
                    break       
                in_file.write(user_input+"\n")
        load_task(filename)




    except FileNotFoundError:
        pass


@app.route('/main')
def main():
    write_tasks(input("Do you want see the current tasks , please write the filename \nWant to create separate To do list , create file:  "))
main()

if __name__=='__main__':
    app.run(debug="True")