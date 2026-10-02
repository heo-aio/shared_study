-- JOIN
-- 둘 이상의 테이블을 연결하여 데이털르 검색하는 방법
-- 둘 사이에 적어도 하나이상의 공통된 컬럼이 존재해야한다.
-- 그래서 일반적으로 부모자식간에 JOIN이 자주 일어난다. (PK-FK)

-- JOIN 방법
-- CROSS JOIN
-- Equi JOIN (등가조인, 내부조인, 내추럴조인)
-- Non Equi JOIN <- 거의 사용하지않음
-- Self JOIN <- 특수한 경우에만 사용
-- OUTER JOIN

-- 0. CROSS JOIN
-- 카다시안 곱 수행
-- emp(10) * dept(4) = 40
-- Equi JOIN에서 조건문이 빠진 형태로 정제되기 전 버전
SELECT e.ename, d.deptname FROM emp e CROSS JOIN dept d;
-- CROSS와 JOIN은 생략가능
SELECT e.ename, d.deptno, d.deptname FROM emp e, dept d;

-- 1. Equi JOIN
-- CROSS JOIN에서 두 테이블이 동일하게 있는 값만을 추출한 형태
-- emp ename이 kim인 사람은 deptno가 1이지? 그러니까 dept에서 deptno 1인 녀석과만 합쳐

-- 1) 등가조인 (가장 기본적인 조인)
SELECT * FROM dept;
SELECT * FROM emp;

SELECT e.ename, d.deptno, d.deptname FROM emp e, dept d
	WHERE e.deptno = d.deptno;
-- dept에는 deptno3이 있다. 하지만 emp에는 deptno 3이 없기때문에 표시되지 않는다.

-- 2) 내부조인(INNER JOIN)
-- 테이블 사이에, 대신 INNER JOIN이 들어간다. (INNER는 생략가능)
-- JOIN의 조건에 WHERE가 아닌 ON절 사용
-- WHERE에 필터링 조건과 조인 조건을 모두 사용하면 혼돈 발생하므로 ON절 사용
SELECT e.ename, d.deptno, d.deptname FROM emp e INNER JOIN dept d
	ON e.deptno = d.deptno;

-- USING을 사용하면 조인에 사용할 컬럼이나 뷰 서브쿼리 등을 사용할 수 있다.
SELECT e.ename, d.deptno, d.deptname FROM emp e JOIN dept d USING(deptno);

-- 3) 내츄럴조인 (NATURAL JOIN)
-- 두 테이블 사이에 공통된 컬럼이 있으면 알아서(자연스럽게) 합친다.
SELECT e.ename, deptno, d.deptname FROM emp e NATURAL JOIN dept d;


-- 2. 외부조인 (OUTER JOIN)
-- Equi JOIN은 두 ㅔ이블 모두에 데이터가 존재해야 보여준다.
-- 외부조인은 어느 한 테이블에만 있는 데이터라해도 보여준다.

-- 등가조인
-- dept에 있는 deptno = 3은 보여주지 않음
SELECT e.ename, d.deptno, d.deptname FROM emp e JOIN dept d
ON e.deptno = d.deptno;

-- 외부조인
-- 두 테이블 중 보여줄 종류가 더 많은 테이블을 지목하는 형태
SELECT e.ename, d.deptno, d.deptname FROM emp e RIGHT OUTER JOIN dept d
ON e.deptno = d.deptno;

-- dept에는 없고 emp에만 있는 deptno를 넣으려고 한다.
-- dept는 emp의 부모이기 때문에 emp에 없는 deptno란 있을 수 없다.
-- 부모자식 관계를 제거할 예정 (FK제거)
-- ALTER TABLE [테이블명] DROP CONSTRAINT [제약조건이름]
SELECT * FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_NAME = "emp";
ALTER TABLE emp DROP CONSTRAINT fk_emp;
DESC emp;

-- emp에 deptno 6을 추가
INSERT INTO emp VALUES("kim", "assistant", 6, STR_TO_DATE("14-06-02", "%Y-%m-%d"));

SELECT * FROM emp;
-- emp에 더 있는 deptno를 기준으로 뽑아보자
SELECT e.ename, e.deptno, d.deptname 
FROM emp e LEFT OUTER JOIN dept d
ON e.deptno = d.deptno;

-- LEFT JOIN + RIGHT JOIN = FULL OUTER JOIN
-- mariaDB에서는 지원하지 않는다. (다른방법이 있어서)
