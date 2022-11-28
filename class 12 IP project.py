import pandas as pd
import mysql.connector as sqLtor
import pymysql
from sqlalchemy import create_engine
import sys
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
mycon=sqLtor.connect(host='localhost',user='root',passwd='kavish24',database='lms')

engine=create_engine('mysql+mysqlconnector://root:kavish24@localhost/lms')
conn=engine.connect()
def main():
    print('Welcome to Library Management System')
    print()
    pd121=pd.read_sql('select * from max_books',mycon)
    val=pd121['books_max'].tolist()
    val1=0
    if(val[0]==0):
        val1=input('Enter Max Books customer can issue: ')
        pd121['books_max']=val1
        mycursor=mycon.cursor()
        sql='delete from max_books;'
        mycursor.execute(sql)
        mycon.commit()
        pd121.to_sql('max_books',conn,index=False,if_exists='append')
        print('UPDATED SUCCESSFULLY')
    pd122=pd.read_sql('select * from fine_rate',mycon)
    val4=pd122['fine_rate'].tolist()
    val5=0
    if(val4[0]==0):
        val5=input('Enter Fine Rate/DAY: ')
        pd122['fine_rate']=val5
        mycursor1=mycon.cursor()
        sql1='delete from fine_rate;'
        mycursor1.execute(sql1)
        mycon.commit()
        pd122.to_sql('fine_rate',conn,index=False,if_exists='append')
        print('UPDATED SUCCESSFULLY')
    pd112=pd.read_sql('select * from max_months',mycon)
    val9=pd112['max_months'].tolist()
    val10=0
    if(val9[0]==0):
        val10=input('Enter Max Months Customer Can keep a Book: ')
        pd112['max_months']=val10
        mycursor2=mycon.cursor()
        sql2='delete from max_months;'
        mycursor2.execute(sql2)
        mycon.commit()
        pd112.to_sql('max_months',conn,index=False,if_exists='append')
        print('UPDATED SUCCESSFULLY')
    print('What would you like to do today: ')
    print('Press 1 to UPDATE BOOK LEDGER')
    print('Press 2 to UPDATE CUSTOMER RECORDS')
    print('Press 3 to ISSUE OR RETURN BOOK')
    print('Press 4 to SEE STATISTICS')
    print('Press 5 to EXIT PROGRAM')
    numb=input('Please enter your no.: ')
    if numb=='1':
        print('Press 1 to ADD NEW BOOK')
        print('Press 2 to REMOVE BOOK')
        print('Press 3 to VIEW ENTIRE BOOK LEDGER')
        print('Press 4 to VIEW SPECIFIC BOOK')
        numb1=input('Please enter your no.: ')
        if(numb1=='1'):
           pd1=pd.DataFrame([[input('Enter Book ID(5 DIGIT Number): '),input('Enter Book Name: ').lower().replace(' ',''),
                              input('Enter Book Genre: ').lower().replace(' ',''),0,0]],columns=['book_id','book_name',
                                                                          'book_genre','cust_id','date_borrowed'])
           pd1.to_sql('book_ledger',conn,index=False,if_exists='append')
           print('Book Successfully Added')
           main()
        elif(numb1=='2'):
            mycursor=mycon.cursor()
            sql='drop table book_ledger;'
            ID=input('Enter Book ID of book to remove: ')
            pd2=pd.read_sql('select * from book_ledger',mycon)
            ind=pd2.index[(pd2['book_id']==ID)]
            pd2.drop(ind,inplace=True)
            mycursor.execute(sql)
            mycon.commit()
            pd2.to_sql('book_ledger',conn,index=False,if_exists='append')
            print('Book Removed Successfully')
            main()
        elif(numb1=='3'):
            print('BOOK LEDGER: ')
            pd3=pd.read_sql('select * from book_ledger',mycon)
            print(pd3)
            main()
        elif(numb1=='4'):
            print('Press 1 to search for book by book_id: ')
            print('Press 2 to search for book by name: ')
            numb2=input('Please enter your number: ')
            if(numb2=='1'):
                l1=input('Enter book_id of desired book: ')
                qrty='select * from book_ledger where book_id=%s;'%(l1,)
                pd4=pd.read_sql(qrty,mycon)
                print('Details of book are: ')
                print(pd4)
                main()
            elif(numb2=='2'):
                l2=input('Enter book_name of desired book: ').lower().replace(' ','')
                print('Details of book are: ')
                pd5=pd.read_sql('select * from book_ledger',mycon)
                ind1=pd5.index[(pd5['book_name']==l2)].tolist()
                k=ind1[0]
                print(pd5.loc[[k]])
                main()
            else:
                print('INVALID INPUT')
                main()
        else:
            print('INVALID INPUT')
            main()
    elif(numb=='2'):
        print('Press 1 to ADD NEW CUSTOMER')
        print('Press 2 to REMOVE CUSTOMER')
        print('Press 3 to SEE CUSTOMER RECORDS')
        print('Press 4 to RENEW MEMBERSHIP')
        inpt=input('Enter your number: ')
        if(inpt=='1'):
            curdate=date.today()
            pd8=pd.DataFrame([[input('Enter Customer Phone no: ').lower().replace(' ',''),input('Enter Customer Name: ').lower().replace(' ',''),
                               curdate,input('Enter how many months activated: '.lower().replace(' ','')),0,0,0]],
                             columns=['cust_id','cust_name','date_activated','months','del_day','del_times','trans_times'])
            pd8.to_sql('cust_ledger',conn,index=False,if_exists='append')
            print('Customer Added Successfully')
            main()
        elif(inpt=='2'):
            mycursor=mycon.cursor()
            sql='drop table cust_ledger;'
            ID=input('Enter Phone Number of Customer to remove: ')
            pd2=pd.read_sql('select * from cust_ledger',mycon)
            ind=pd2.index[(pd2['cust_id']==ID)]
            pd2.drop(ind,inplace=True)
            mycursor.execute(sql)
            mycon.commit()
            pd2.to_sql('cust_ledger',conn,index=False,if_exists='append')
            print('Customer Removed Successfully')
            main()
        elif(inpt=='3'):
            pd10=pd.read_sql('select * from cust_ledger;',mycon)
            print(pd10)
            main()
        elif(inpt=='4'):
            curdate=date.today()
            custid=input('Enter Phone no. of customer to Renew: ')
            pdsq1=pd.read_sql('select * from cust_ledger',mycon)
            ind=pdsq1.index[(pdsq1['cust_id']==custid)].tolist()
            months=input('Enter no. of months to renew: ')
            pdsq1.months[ind]=months
            pdsq1.date_activated[ind]=curdate
            mycursor=mycon.cursor()
            sql='delete from cust_ledger;'
            mycursor.execute(sql)
            mycon.commit()
            pdsq1.to_sql('cust_ledger',conn,index=False,if_exists='append')
            print('Membership Renewed Successfully')
            main()
        else:
            print('INVALID INPUT')
            main()
    elif(numb=='3'):
            print('Press 1 to ISSUE BOOK')
            print('Press 2 to RETURN BOOK')
            print('Press 3 to EDIT MAX BOOKS')
            print('Press 4 to EDIT FINE RATE/DAY')
            print('Press 5 to EDIT MAX MONTHS CUSTOMER CAN KEEP A BOOK')
            inpt1=input('Enter your chosen number: ')
            if(inpt1=='1'):
                custid=input('Enter Phone no of customer to issue: ')
                pdsq=pd.read_sql('select * from book_ledger;',mycon)
                pdsq1=pd.read_sql('select * from cust_ledger',mycon)
                print('Press 1 to ISSUE BOOK')
                k2=input('Enter your chosen number: ')
                max_booksdf=pd.read_sql('select * from max_books;',mycon)
                max_books=max_booksdf.books_max[0]
                curdate=date.today()
                ind2=pdsq1.index[(pdsq1['cust_id']==custid)].tolist()
                #membership=pdsq1.date_activated[ind2[0]]
                membership=pdsq1.date_activated[ind2[0]]
                ind3=pdsq1.index[(pdsq1['cust_id']==custid)].tolist()
                months=pdsq1.months[ind3[0]]
                days=months*30
                diff=curdate-membership
                difference=diff.days
                if(difference>days):
                    print('MEMBERSHIP HAS EXPIRED, RENEW MEMBERSHIP to borrow book')
                    main()
                if(k2=='1'):
                    bookid=input('Enter ID of book to issue: ')
                    check=pdsq[pdsq['cust_id']==custid]
                    listo=[]
                    listo=list(check.shape)
                    if(listo[0]>=max_books):
                        print('Customer has already borrowed max allowed books, return a book to issue new one')
                        main()
                    else:
                        ind4=pdsq.index[(pdsq['book_id']==bookid)].tolist()
                        pdsq.cust_id[ind4[0]]=custid
                        pdsq.date_borrowed[ind4[0]]=curdate
                        mycursor=mycon.cursor()
                        sql='delete from book_ledger;'
                        mycursor.execute(sql)
                        mycon.commit()
                        pdsq.to_sql('book_ledger',conn,index=False,if_exists='append')
                        print('Book Issued Successfully')
                        main()
                else:
                    print('INVALID INPUT')
                    main()
            elif(inpt1=='2'):
                print('yO')
                custid=input('Enter Phone no of customer to Return: ')
                pdsq=pd.read_sql('select * from book_ledger;',mycon)
                pdsq1=pd.read_sql('select * from cust_ledger',mycon)
                max_monthsdf=pd.read_sql('select * from max_months;',mycon)
                max_months=max_monthsdf.max_months[0]
                fine_ratedf=pd.read_sql('select * from fine_rate;',mycon)
                fine_rate=fine_ratedf.fine_rate[0]
                bookid=input('Enter Book ID of Book to Return: ')
                curdate=date.today()
                ind1=pdsq1.index[(pdsq1['cust_id']==custid)].tolist()
                ind=pdsq.index[(pdsq['book_id']==bookid)].tolist()
                max_days=max_months*30
                date_borrowed=pdsq.date_borrowed[ind[0]]
                diff=curdate-date_borrowed
                difference=diff.days
                if(difference>max_days):
                    del_days=difference-max_days
                    fine=del_days*fine_rate
                    print('Fine Applicable: ',fine)
                    delold=pdsq1.del_day[ind1[0]]
                    transold=pdsq1.trans_times[ind1[0]]
                    del_timesold=pdsq1.del_times[ind1[0]]
                    transnew=transold+1
                    delnew=(delold+del_days)/transnew
                    del_timesnew=del_timesold+1
                    pdsq1.del_times[ind1[0]]=del_timesnew
                    pdsq1.del_day[ind1[0]]=delnew
                    pdsq1.trans_times[ind1[0]]=transnew
                    pdsq.date_borrowed[ind[0]]=0
                    pdsq.cust_id[ind[0]]=0
                    mycursor=mycon.cursor()
                    sql='delete from book_ledger;'
                    mycursor.execute(sql)
                    mycon.commit()
                    mycursor1=mycon.cursor()
                    sql1='delete from cust_ledger;'
                    mycursor1.execute(sql1)
                    mycon.commit()
                    pdsq.to_sql('book_ledger',conn,index=False,if_exists='append')
                    pdsq1.to_sql('cust_ledger',conn,index=False,if_exists='append')
                    print('Book Returned Successfully')
                    main()
                else:
                    transold=pdsq1.trans_times[ind1]
                    transnew=transold+1
                    pdsq.date_borrowed[ind]=0
                    pdsq.cust_id[ind]=0
                    pdsq1.trans_times[ind1]=transnew
                    mycursor=mycon.cursor()
                    sql='delete from book_ledger;'
                    mycursor.execute(sql)
                    mycon.commit()
                    mycursor1=mycon.cursor()
                    sql1='delete from cust_ledger;'
                    mycursor1.execute(sql1)
                    mycon.commit()
                    pdsq.to_sql('book_ledger',conn,index=False,if_exists='append')
                    pdsq1.to_sql('cust_ledger',conn,index=False,if_exists='append')
                    print('Book Returned Successfully')
                    main()       
            elif(inpt1=='3'):
                pd123=pd.read_sql('select * from max_books;',mycon)
                l=input('Enter Max Books that can be issued: ')
                pd123['books_max']=l
                mycursor=mycon.cursor()
                sql='delete from max_books;'
                mycursor.execute(sql)
                mycon.commit()
                pd123.to_sql('max_books',conn,index=False,if_exists='append')
                print('UPDATED SUCCESSFULLY')
                main()
            elif(inpt1=='4'):
                pd123=pd.read_sql('select * from fine_rate;',mycon)
                l=input('Enter Fine Rate/DAY: ')
                pd123['fine_rate']=l
                mycursor=mycon.cursor()
                sql='delete from fine_rate;'
                mycursor.execute(sql)
                mycon.commit()
                pd123.to_sql('fine_rate',conn,index=False,if_exists='append')
                print('UPDATED SUCCESSFULLY')
                main()
            elif(inpt1=='5'):
                pd123=pd.read_sql('select * from max_months;',mycon)
                l=input('Enter Max Months Customer Can Keep A Book: ')
                pd123['max_months']=l
                mycursor=mycon.cursor()
                sql='delete from max_months;'
                mycursor.execute(sql)
                mycon.commit()
                pd123.to_sql('max_months',conn,index=False,if_exists='append')
                print('UPDATED SUCCESSFULLY')
                main()
            else:
                print('INVALID INPUT')
                main()
    elif(numb=='4'):
        print('Press 1 to SEE GRAPH SHOWING PERCENTAGE OF TIMES CUSTOMER IS LIKELY TO DELAY RETURN')
        print('Press 2 to SEE GRAPH SHOWING TRANSACTION TIMES OF ALL CUSTOMERS')
        print('Press 3 to SEE GRAPH SHOWING NUMBER OF DAYS CUSTOMERS ARE LIKEY TO DELAY')
        pdsq1=pd.read_sql('select * from cust_ledger;',mycon)
        inp=input('Enter your chosen number: ')
        delday=np.array(pdsq1.del_day[:])
        deltimes=np.array(pdsq1.del_times[:])
        transtimes=np.array(pdsq1.trans_times[:])
        percdeltimes=(deltimes/transtimes)*100
        custid=np.array(pdsq1.cust_id[:])
        if(inp=='1'):
            plt.bar(custid,percdeltimes,color='g',align='center',width=0.5)
            plt.xlabel('Customer Phone')
            plt.ylabel('% Times Delayed')
            plt.show()
            main()
        elif(inp=='2'):
            plt.bar(custid,transtimes,color='g',align='center',width=0.5)
            plt.xlabel('Customer Phone')
            plt.ylabel('Transaction Times')
            plt.show()
            main()
        elif(inp=='3'):
            plt.bar(custid,delday,color='g',align='center',width=0.5)
            plt.xlabel('Customer Phone')
            plt.ylabel('Average Days Delayed')
            plt.show()
            main()
        else:
            print('INVALID INPUT')
            main()
    elif(numb=='5'):
        print('Thank You For Using Library Management System')
        sys.exit() 
    else:
        print('INVALID INPUT')
        
if __name__=='__main__':
    main()
