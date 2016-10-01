from discord.ext import commands


def predicate(ctx, perms):
    msg = ctx.message
    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)

    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def check(**perms):
    return commands.check(lambda ctx: predicate(ctx, perms))
