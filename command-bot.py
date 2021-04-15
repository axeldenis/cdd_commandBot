import discord
from discord import embeds

PASSER_COMMANDE_ID = 815339353365544981
CHANNEL_COMMANDES_ID = 688084123725725800
CHANNEL_ERREURS_ID = 815344478784454667

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


# menus et embeds constants
PREMIER_EMBED = discord.Embed(title="Passer une annonce",description="Salut ! Je suis le bot de Coin Des Devs, nous allons configurer ton annonce, fais bien attention à respecter les indiquations que je te donnerais ^^\nCa ne sera pas long !")
PREMIER_EMBED.add_field(name="Un beau titre",value="Commence par définir un titre à ta commande. Fais le court et précis !\nAttention, le prochain message que tu enverras sera mis en titre !")
PREMIER_EMBED.set_footer(text="Cette demande expire dans 10 minutes.")

SECOND_EMBED = discord.Embed(title="Continuons ton annonce",description="Maintenant, il nous faut une description pour ton annonce ! Suis les consignes ci dessous pour la faire le mieux possible.\nAttention, ton prochain message sera considéré comme une réponse !\nIMPORTANT : Elle doit faire 1024 caractères ou moins (limitation de discord). Les émojis et mentions prennent beaucoup de place alors il est déconseillé de les utiliser.")
SECOND_EMBED.add_field(name="Le contexte de ton annonce :",value="Dans ce premier message, parle du contexte de ton annonce. (Le projet général dans lequel se place le programme que tu demandes par exemple)")
SECOND_EMBED.set_footer(text="Cette demande expire dans 10 minutes.")

TROISIEME_EMBED = discord.Embed(title="Continuons ton annonce",description="Maintenant, il nous faut une description pour ton annonce ! Suis les consignes ci dessous pour la faire le mieux possible.\nAttention, ton prochain message sera considéré comme une réponse !\nIMPORTANT : Elle doit faire 1024 caractères ou moins (limitation de discord). Les émojis et mentions prennent beaucoup de place alors il est déconseillé de les utiliser.")
TROISIEME_EMBED.add_field(name="Le programme que tu veux précisément",value="Maintenant, sois précis et parle du programme que tu veux, par exemple, un programme __python__ qui fait __telle chose__... Toujours en 1024 caractères max !")
TROISIEME_EMBED.set_footer(text="Cette demande expire dans 10 minutes.")

QUATRIEME_EMBED = discord.Embed(title="Domaine de ta demande",description="Indique si possible le(s) langage(s) voulu(s) pour ta commande. Si tu laisse libre ce choix, tu peux au moins citer le domaine, par exemple l'OS.\nSinon répond `x`")
QUATRIEME_EMBED.add_field(name="Attention",value="La longueur maximale acceptée pour ta réponse est 25 lettres.")
QUATRIEME_EMBED.add_field(name="Exemples :",value="Site Web\nJeu Vidéo\nBot Discord\nC++\nPHP\n...")

CINQUIEME_EMBED = discord.Embed(title="Prix de ta demande",description="Indique ton budget, tu peux donner un intervale si besoin.")
CINQUIEME_EMBED.add_field(name="Consignes",value="**Ton prix doit respecter les tendances de prix indiquées dans #dev-pub par les développeurs.**\nNous ne travaillerons pas pour des sommes anormalement faibles.\n Il est conseillé de regarder les propositions dans #dev-pub pour se faire une idée des prix et services.")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(reaction):

    if reaction.channel_id == PASSER_COMMANDE_ID and not reaction.member == client.user: # quand il y a réaction, on va voir avec le client pour passer commande | accepte toutes les réactions sur n'importe quel message du channel
        
        channel = client.get_channel(PASSER_COMMANDE_ID)
        message = await channel.fetch_message(reaction.message_id)
        await message.remove_reaction(reaction.emoji, reaction.member) #on retire sa réaction

        try: # un try pour les utilisateurs aux dm fermés
            dm = reaction.member.dm_channel
            if dm == None:
                await reaction.member.create_dm()
                dm = reaction.member.dm_channel
            await dm.send(embed=PREMIER_EMBED)

        except Exception as err:
            print(err)
            await client.get_channel(CHANNEL_ERREURS_ID).send("<@" + str(reaction.member.id) + ">, tu dois ouvrir tes dm pour que nous puissions y configurer ta commande.\n(tu pourras bien sur les refermer quand nous aurons fini)")
            return # on ne vas pas plus loin
        
        def check(message):
            return len(message.content) <= 1024 and message.channel == dm and message.author != client.user
        
        try:
            message = await client.wait_for("message",check=check,timeout=600)
        except Exception as err:
            #print(err)
            await dm.send("Ta demande a expiré... Tu pourras toujours en refaire une ^^")
            return # on ne va pas plus loin
        
        await dm.send('Ok, titre mis à "' + message.content + '" !')
        titre = message.content
        await dm.send(embed=SECOND_EMBED)

        try:
            message = await client.wait_for("message",check=check,timeout=600)
        except Exception as err:
            #print(err)
            await dm.send("Ta demande a expiré... Tu pourras toujours en refaire une ^^")
            return # on ne va pas plus loin
        
        await dm.send("Ok, j'ai pris en compte ta réponse.")
        description_projet = message.content
        await dm.send(embed=TROISIEME_EMBED)

        try:
            message = await client.wait_for("message",check=check,timeout=600)
        except Exception as err:
            #print(err)
            await dm.send("Ta demande a expiré... Tu pourras toujours en refaire une ^^")
            return # on ne va pas plus loin
        
        await dm.send("Ok, j'ai pris en compte ta réponse.")
        description_programme = message.content

        await dm.send(embed=QUATRIEME_EMBED)
        
        
        try:  # la ligne suivante est un peu sale mais c'est juste une redéfinition de check avec 25 comme longueur max
            message = await client.wait_for("message",check=lambda msg:len(msg.content) <= 25 and msg.channel == dm and msg.author != client.user,timeout=600)
        except Exception as err:
            await dm.send("Ta demande a expiré... Tu pourras toujours en refaire une ^^")
            return # on ne va pas plus loin
        
        await dm.send("Ok, j'ai pris en compte ta réponse : " + message.content)
        domaine_commande = message.content

        await dm.send(embed=CINQUIEME_EMBED)
        
        
        try:  # la ligne suivante est un peu sale mais c'est juste une redéfinition de check avec 25 comme longueur max
            message = await client.wait_for("message",check=lambda msg:len(msg.content) <= 25 and msg.channel == dm and msg.author != client.user,timeout=600)
        except Exception as err:
            await dm.send("Ta demande a expiré... Tu pourras toujours en refaire une ^^")
            return # on ne va pas plus loin
        
        await dm.send("Ok, j'ai pris en compte ta réponse : " + message.content)
        prix_commande = message.content

        temp_embed = discord.Embed(title=titre,description=description_projet,color=int(str(message.id)[-7:]))
        temp_embed.set_thumbnail(url=message.author.avatar_url)
        temp_embed.add_field(name="Programme demandé :",value = description_programme,inline=False)
        temp_embed.add_field(name="Domaine :",value = domaine_commande)
        temp_embed.add_field(name="Budget :",value = prix_commande)
        await dm.send(embed=temp_embed)
        await dm.send("Ok tout est setup, tu peux vérifier l'aspect final juste au dessus. Pour l'envoyer, fais `send`.\nSinon cette demande expirera dans 1 minute.")
        
        try:  # la ligne suivante est un peu sale mais c'est juste une redéfinition de check avec 25 comme longueur max
            message = await client.wait_for("message",check=lambda msg:msg.content == "send" and msg.channel == dm and msg.author != client.user,timeout=60)
        except Exception as err:
            await dm.send("Ta demande a expiré... Tu pourras toujours en refaire une ^^")
            return # on ne va pas plus loin

    cmdChannel = client.get_channel(CHANNEL_COMMANDES_ID)
    await cmdChannel.send("**__Commande de :__** <@" + str(message.author.id) + ">",embed=temp_embed)

        




@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content == "test":
        await message.channel.send(str(message.channel.id))

client.run('')
