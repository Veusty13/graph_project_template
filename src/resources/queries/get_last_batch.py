query = """select
    step :: int as step,
    type :: char as type,
    amount :: float as amount,
    nameOrig :: varchar as nameOrig,
    oldbalanceOrg :: float as oldbalanceOrg,
    newbalanceOrig :: float as newbalanceOrig,
    nameDest :: varchar as nameDest,
    oldbalanceDest :: float as oldbalanceDest,
    newbalanceDest :: float as newbalanceDest,
    isFraud :: int as isFraud,
    isFlaggedFraud :: int as isFlaggedFraud
    from
    transactions
    where batch_id = {};"""
