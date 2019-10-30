#-*-coding:utf-8-*-
#!/usr/bin/python
import threading,time

def son_1(i,j):
        print('start son_threading%d fa_%d\n' %(j,i))
        time.sleep(3)
        print('end son_threading%d fa_%d\n' %(j,i))

def father_t(i,j):
    print('start fa_t%d\n' % i)
    t1s=[]
    for jj in range(j):
        t1=threading.Thread(target=son_1,args=(i,jj))
        t1.start()
        t1s.append(t1)
        time.sleep(2)
    for t1 in t1s:
        t1.join()
    print('end fa_t%d\n' % i)

if __name__=='__main__':
    t2s=[]
    for i in range(2):
        t2=threading.Thread(target=father_t,args=(i,15))
        t2.start()
        t2s.append(t2)
    for t2 in t2s:
        t2.join()

