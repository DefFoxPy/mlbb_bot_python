import discord
import config
from discord.ext import commands
import networkx as nx
import matplotlib.pyplot as plt

# Configura el bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True 

prefix = "!z"

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id=config.APPLICATION_ID)

# Diccionario para almacenar las menciones
mentions = {}

@bot.event
async def on_ready():
    activity = discord.Game(name='Bot bug dance', type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def generar_grafo(ctx, canal: discord.TextChannel):
    # Limpiar el diccionario de menciones
    mentions.clear()

    # Obtener los mensajes del canal especificado
    print(f"Analizando mensajes en el canal: {canal.name}")
    async for message in canal.history(limit=config.LIMIT):
        if message.mentions:
            print(f"Mensaje de {message.author}: {message.content}")
            author = message.author
            for mentioned_user in message.mentions:
                if author != mentioned_user:
                    key = (author.id, mentioned_user.id)
                    mentions[key] = mentions.get(key, 0) + 1
                    print(f"Mención registrada: {author} -> {mentioned_user}")

    # Verificar si hay menciones
    if not mentions:
        await ctx.send("No se encontraron menciones en el historial del canal. No se puede crear el grafo.")
        return

    # Crear el grafo
    G = nx.DiGraph()

    # Añadir nodos y arcos al grafo
    for (author_id, mentioned_id), weight in mentions.items():
        # Obtener el nombre del autor
        author = ctx.guild.get_member(author_id)
        if author is None:
            print(f"Usuario con ID {author_id} no encontrado. Ignorando...")
            continue  # Ignorar si el usuario no está en el servidor

        # Obtener el nombre del usuario mencionado
        mentioned = ctx.guild.get_member(mentioned_id)
        if mentioned is None:
            print(f"Usuario mencionado con ID {mentioned_id} no encontrado. Ignorando...")
            continue  # Ignorar si el usuario mencionado no está en el servidor

        # Añadir la arista al grafo
        G.add_edge(author.name, mentioned.name, weight=weight)
        print(f"Arista añadida: {author.name} -> {mentioned.name} (peso: {weight})")

    # Verificar si el grafo tiene aristas
    if G.number_of_edges() == 0:
        await ctx.send("No se encontraron menciones válidas para crear el grafo.")
        return

    # Dibujar el grafo
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # Ajustar el layout para evitar superposiciones
    plt.figure(figsize=(14, 10))

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="skyblue", alpha=0.9)

    # Dibujar aristas con colores personalizados
    edge_colors = []
    for u, v in G.edges():
        if G.has_edge(v, u):  # Si hay una mención bidireccional
            edge_colors.append("red")  # Flecha roja para menciones bidireccionales
        else:
            edge_colors.append("gray")  # Flecha gris para menciones unidireccionales

    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle="->", arrowsize=20, width=2)

    # Dibujar etiquetas de los nodos
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="darkblue")

    # Dibujar etiquetas de las aristas (pesos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    # Añadir un título al grafo
    plt.title(f"Grafo de menciones en #{canal.name}", fontsize=16, fontweight="bold")

    # Guardar la imagen del grafo
    plt.savefig("grafo.png", bbox_inches="tight", dpi=300)
    plt.close()

    # Enviar la imagen al canal
    await ctx.send(file=discord.File("grafo.png"))

# Reemplaza 'TU_TOKEN' con el token de tu bot
bot.run(config.TOKEN)