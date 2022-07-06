CREATE_TABLE_COMPANY = (
        'CREATE TABLE company (' +
        'cnpj TEXT NOT NULL,' +
        'uf TEXT NOT NULL,' +
        'import_date TEXT NOT NULL );'
)
CREATE_TABLE_REQUEST_STACK = (
        'CREATE TABLE request_stack (' +
        'id INTEGER PRIMARY KEY NOT NULL,' +
        'uf CHAR(2) NOT NULL,' +
        'num_thread INT,' +
        'dt_hr_scheduled DATETIME NOT NULL DEFAULT (datetime() ),' +
        'dt_hr_inclusion DATETIME NOT NULL DEFAULT (datetime() ),' +
        'dt_hr_end DATETIME,' +
        'status TEXT DEFAULT pendente NOT NULL,' +
        'num_cnpj_bd        BIGINT,' +
        'num_cnpj_processed BIGINT,' +
        'num_ie_found       BIGINT,' +
        'num_ie_not_found   BIGINT );'
)
CREATE_TABLE_IE = (
        'CREATE TABLE ie (' +
        'cnpj TEXT (14),' +
        'ie TEXT (20),' +
        'razao_social TEXT (255),' +
        'uf CHAR (2),' +
        'cod_sit INT,' +
        'situacao TEXT (255),'
        'record_dt_hr DATETIME,' +
        'PRIMARY KEY ( cnpj, ie )'
        'ON CONFLICT REPLACE);'
)
