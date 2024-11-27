TRUNCATE TABLE STG.LEGAL_PARTY_VIEW_FUNCTION;

INSERT INTO STG.LEGAL_PARTY_VIEW_FUNCTION
SELECT 
*
FROM (SELECT 
        "field_1",
        "field_2",
        "field_3",
        "field_4",
        "field_5",
        "field_6",
        "field_7",
        "field_8",
        "field_9",
        "field_10",
        "field_11",
        "field_12",
        "field_13",
        "field_14",
        "field_15",
        "field_16",
        "field_17",
        "field_18",
        "field_19"
FROM
(
IMPORT FROM JDBC AT POSTGRES_CONN
        STATEMENT
        'SELECT *
         FROM stg.legal_party_view_function(&month_l,&year_l)'
)        
);

TRUNCATE TABLE STG.PHYSICAL_VIEW_FUNCTION;

INSERT INTO STG.PHYSICAL_VIEW_FUNCTION
SELECT 
*
FROM (SELECT 
        "field_1",
        "field_2",
        "field_3",
        "field_4",
        "field_5",
        "field_6",
        "field_7",
        "field_8",
        "field_9",
        "field_10",
        "field_11",
        "field_12",
        "field_13",
        "field_14",
        "field_15",
        "field_16",
        "field_17",
        "field_18",
        "field_19",
        "field_20",
        "field_21"
FROM
(
IMPORT FROM JDBC AT POSTGRES_CONN
        STATEMENT
        'SELECT *
         FROM stg.physical_view_function(&month_p,&year_p)'
)        
);
