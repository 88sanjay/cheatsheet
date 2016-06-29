# Get list of recipients who have got transfers totalling more than 300$ in at most 3 transactions
SELECT recipient FROM (
	SELECT recipient,SUM(amount) AS TOT FROM (
 		SELECT  A.*,
   			(SELECT COUNT(DISTINCT(B.amount))
   			FROM transfers B
 		WHERE B.amount >= A.amount and A.recipient=B.recipient) as Rank FROM  transfers A
	) AS C WHERE C.Rank <=3 GROUP BY C.recipient 
) WHERE TOT > 300 ORDER BY recipient ASC 


