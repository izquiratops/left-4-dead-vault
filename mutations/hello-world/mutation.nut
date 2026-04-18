// Hello World — minimal mutation template

// Director controls spawning, pacing, and mob density
DirectorOptions <-
{
    // Inherit all defaults. Uncomment to override:
    // CommonLimit   = 30
    // MobMaxPending = 10
}

// Called once when the round starts
function OnGameplayStart()
{
    Msg( "[HelloWorld] Mutation active.\n" )
}

// Called each game frame — uncomment only if needed, it's expensive
// function Think()
// {
// }
