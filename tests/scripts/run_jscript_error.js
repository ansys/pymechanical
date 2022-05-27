function getIsDistributed()
{
    return DS.Script.isDistributed();
}

function test()
{
    return "test";
}

getIsDistributed();

b = a + 1;

test();
