# To fetch ALTERNATE records from a table. (EVEN NUMBERED)
select * from emp where rowid in (select decode(mod(rownum,2),0,rowid, null) from emp);

#To select ALTERNATE records from a table. (ODD NUMBERED)
select * from emp where rowid in (select decode(mod(rownum,2),0,null ,rowid) from emp);

#Find the 3rd MAX salary in the emp table.
select distinct sal from emp e1 where 3 = (select count(distinct sal) from emp e2 where e1.sal <= e2.sal);

#Find the 3rd MIN salary in the emp table.
select distinct sal from emp e1 where 3 = (select count(distinct sal) from emp e2where e1.sal >= e2.sal);

#Select FIRST n records from a table.
select * from emp where rownum <= &n;

#Select LAST n records from a table
select * from emp minus select * from emp where rownum <= (select count(*) - &n from emp);

#List dept no., Dept name for all the departments in which there are no employees in the department.
select * from dept where deptno not in (select deptno from emp);  
#alternate solution:  
select * from dept a where not exists (select * from emp b where a.deptno = b.deptno);
#altertnate solution:  
select empno,ename,b.deptno,dname from emp a, dept b where a.deptno(+) = b.deptno and empno is null;


#Select DISTINCT RECORDS from emp table.
select * from emp a where  rowid = (select max(rowid) from emp b where  a.empno=b.empno);

#How to delete duplicate rows in a table?
delete from emp a where rowid != (select max(rowid) from emp b where  a.empno=b.empno);

#Count of number of employees in  department  wise.
select count(EMPNO), b.deptno, dname from emp a, dept b  where a.deptno==b.deptno  group by b.deptno,dname;
 
#Suppose there is annual salary information provided by emp table. How to fetch monthly salary of each and every employee?

select ename,sal/12 as monthlysal from emp;

#Select all record from emp table where deptno =10 or 40.

select * from emp where deptno=30 or deptno=10;

#Select all record from emp table where deptno=30 and sal>1500.

select * from emp where deptno=30 and sal>1500;

#Select  all record  from emp where job not in SALESMAN  or CLERK.

select * from emp where job not in ('SALESMAN','CLERK');

#Select all record from emp where ename in 'BLAKE','SCOTT','KING'and'FORD'.

select * from emp where ename in('JONES','BLAKE','SCOTT','KING','FORD');

#Select all records where ename starts with ‘S’ and its lenth is 6 char.

select * from emp where ename like'S____';

#Select all records where ename may be any no of  character but it should end with ‘R’.

select * from emp where ename like'%R';

#Count  MGR and their salary in emp table.

select count(MGR),count(sal) from emp;

#In emp table add comm+sal as total sal  .

select ename,(sal+nvl(comm,0)) as totalsal from emp;

#Select  any salary <3000 from emp table. 

select * from emp  where sal> any(select sal from emp where sal<3000);

#Select  all salary <3000 from emp table. 

select * from emp  where sal> all(select sal from emp where sal<3000);

#Select all the employee  group by deptno and sal in descending order.

select ename,deptno,sal from emp order by deptno,sal desc;

#How can I create an empty table emp1 with same structure as emp?

Create table emp1 as select * from emp where 1=2;

#How to retrive record where sal between 1000 to 2000?
Select * from emp where sal>=1000 And  sal<2000

#Select all records where dept no of both emp and dept table matches.
select * from emp where exists(select * from dept where emp.deptno=dept.deptno)

#If there are two tables emp1 and emp2, and both have common record. How can I fetch all the recods but common records only once?
(Select * from emp) Union (Select * from emp1)

#How to fetch only common records from two tables emp and emp1?
(Select * from emp) Intersect (Select * from emp1)

#How can I retrive all records of emp1 those should not present in emp2?
(Select * from emp) Minus (Select * from emp1)

#Count the totalsa  deptno wise where more than 2 employees exist.
SELECT  deptno, sum(sal) As totalsal
FROM emp
GROUP BY deptno
HAVING COUNT(empno) > 2

