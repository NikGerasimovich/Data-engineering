WITH cte AS (
SELECT 
        a.DGL_ENTRY_SID,
        a.ENTRY_DATE AS PERIOD,
        a.ACCOUNT_DT_SID,
        a.ACCOUNT_CR_SID,
        a.CURRENCY_SID,
        a.AMOUNT AS AMOUNT_DT,
        a.AMOUNT AS AMOUNT_CR,
        a.AMOUNT_BASE,
        a.AMOUNT_NU_DT,
        a.AMOUNT_NU_CR,
        a.AMOUNT_VR_DT,
        a.AMOUNT_VR_CR,
        a.AMOUNT_PR_DT,
        a.AMOUNT_PR_CR,
        a.OPERATION_CONTENT,
        a.AGL_ENTRY_SID,
        a.COMPANY_SID,
        a.SYSTEM_SID ,
FROM TABLE_1 a	
)
,
cte1 as (
SELECT 
        a.DGL_ENTRY_SID,
        a.AGL_ENTRY_SID,
        a.PERIOD,
        a.ACC_ENTRY_REG,
        a.ACC_ENTRY_RECNO,
        a.ACCOUNT_DT_SID,
        a.ACCOUNT_CR_SID,
        a.CURRENCY_SID,
        a.AMOUNT_DT,
        a.AMOUNT_CR,
        a.AMOUNT_BASE,
        a.AMOUNT_NU_DT,
        a.AMOUNT_NU_CR,
        a.AMOUNT_VR_DT,
        a.AMOUNT_VR_CR,
        a.AMOUNT_PR_DT,
        a.AMOUNT_PR_CR,
        a.OPERATION_CONTENT,
FROM cte a
JOIN TABLE_2 sys ON sys.SYSTEM_SID = a.SYSTEM_SID
JOIN TABLE_3 c ON c.COMPANY_SID = a.COMPANY_SID  
WHERE (sys.PARENT_SYSTEM_SID = (SELECT SYSTEM_SID FROM AMS_GL.SOURCE_SYSTEM WHERE UPPER(SYSTEM_NAME) = 'SYSTEM_NAME'))
AND c.COMPANY_CODE = 'COMPANY' AND (a.PERIOD >= @start_date AND a.PERIOD < @end_date)
)
SELECT 
        a.DGL_ENTRY_SID,
        a.ACC_ENTRY_REG,
        a.ACC_ENTRY_RECNO,
        a.PERIOD,
        a.ACCOUNT_DT_SID,
        a.ACCOUNT_CR_SID,
        ga.ACC_NUMBER AS ACCOUNT_DT,
        ca.ACC_NUMBER AS ACCOUNT_CR,
        CASE 
        	WHEN a.CURRENC_D IS NULL THEN NULL
        	ELSE c.CURRENCY_CODE
        END AS CURRENCY_CODE_DT ,
        CASE 
        	WHEN a.CURRENCY_C IS NULL THEN NULL
        	ELSE c.CURRENCY_CODE
        END AS CURRENCY_CODE_СR ,       
                CASE 
        	WHEN a.AMOUNT_D IS NULL THEN NULL
        	ELSE a.AMOUNT_DT
        END AS AMOUNT_DT ,        
        CASE 
        	WHEN a.AMOUNT_C IS NULL THEN NULL
        	ELSE a.AMOUNT_CR
        END AS AMOUNT_CR ,
        a.AMOUNT_BASE,
        a.AMOUNT_NU_DT,
        a.AMOUNT_NU_CR,
        a.AMOUNT_VR_DT,
        a.AMOUNT_VR_CR,
        a.AMOUNT_PR_DT,
        a.AMOUNT_PR_CR,
        a.OPERATION_CONTENT
FROM cte1 a
LEFT JOIN TABLE_4 ga ON a.ACCOUNT_DT_SID = ga.GL_ACCOUNT_SID
LEFT JOIN TABLE_5 ca ON a.ACCOUNT_CR_SID = ca.GL_ACCOUNT_SID
LEFT JOIN TABLE_6 c ON a.CURRENCY_SID = c.CURRENCY_SID
