from discord.ext import commands


def checks(_id='205346839082303488'):
    def _is(message, _id):
        if message.author.id == _id:
            return True
        else:
            print('RESTRICTED', message.author, message.content)
            return False

    return commands.check(lambda ctx: _is(ctx.message, _id))

def predicate(ctx, perms):
    msg = ctx.message
    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)

    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def check(**perms):
    return commands.check(lambda ctx: predicate(ctx, perms))