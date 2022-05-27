function getIsDistributed()
{
    return DS.Script.isDistributed();
}

function test()
{
    return "test";
}

getIsDistributed();

test();
