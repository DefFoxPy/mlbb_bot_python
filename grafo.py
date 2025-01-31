import discord
import config
from discord.ext import commands
import networkx as nx
import matplotlib.pyplot as plt

# Cambiar la fuente predeterminada
plt.rcParams['font.family'] = 'DejaVu Sans'

# Configura el bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True 

prefix = "z!"

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id=config.APPLICATION_ID)

# Diccionario para almacenar las menciones
mentions = {}

@bot.event
async def on_ready():
    activity = discord.Game(name='Bot bug dance', type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def generar_grafo(ctx, canal: discord.TextChannel, limit=config.LIMIT, k_value=1.5, x_size=14, y_size=10):
    # Limpiar el diccionario de menciones
    mentions.clear()

    # Obtener los mensajes del canal especificado
    print(f"Analizando mensajes en el canal: {canal.name}")
    async for message in canal.history(limit=limit):
        if message.mentions:
            #print(f"Mensaje de {message.author}: {message.content}")
            author = message.author
            for mentioned_user in message.mentions:
                if author != mentioned_user:
                    key = (author.id, mentioned_user.id)
                    mentions[key] = mentions.get(key, 0) + 1
                    #print(f"Mención registrada: {author} -> {mentioned_user}")

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
            print(f"Usuario con ID {author_id} no encontrado en el servidor. Ignorando...")
            continue  # Ignorar si el usuario no está en el servidor

        # Obtener el nombre del usuario mencionado
        mentioned = ctx.guild.get_member(mentioned_id)
        if mentioned is None:
            print(f"Usuario mencionado con ID {mentioned_id} no encontrado en el servidor. Ignorando...")
            continue  # Ignorar si el usuario mencionado no está en el servidor

        # Añadir la arista al grafo
        G.add_edge(author.name, mentioned.name, weight=weight)
        print(f"Arista añadida: {author.name} -> {mentioned.name} (peso: {weight})")

    # Verificar si el grafo tiene aristas
    if G.number_of_edges() == 0:
        await ctx.send("No se encontraron menciones válidas para crear el grafo.")
        return

    # Dibujar el grafo
    pos = nx.spring_layout(G, k=k_value, iterations=100)  # Aumentar k para separar más los nodos
    plt.figure(figsize=(x_size, y_size))  # Aumentar el tamaño de la figura

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="skyblue", alpha=0.9)

    # Encontrar el arco con el mayor peso
    max_weight = max(weight for _, _, weight in G.edges(data='weight'))
    max_edge = next((u, v) for u, v, weight in G.edges(data='weight') if weight == max_weight)

    # Dibujar aristas con colores personalizados, forma de arco y grosor proporcional al peso
    edge_colors = []
    edge_styles = []
    edge_widths = []
    for u, v in G.edges():
        weight = G[u][v]['weight']

        if (u, v) == max_edge or (v, u) == max_edge:  # Si es el arco con el mayor peso
            edge_colors.append("green")  # Flecha verde para el arco más pesado
        elif G.has_edge(v, u):  # Si hay una mención bidireccional
            edge_colors.append("red")  # Flecha roja para menciones bidireccionales
        else:
            edge_colors.append("gray")  # Flecha gris para menciones unidireccionales

        if G.has_edge(v, u):  # Forma de arco para evitar superposiciones
            edge_styles.append("arc3,rad=0.2")
        else:
            edge_styles.append("arc3,rad=0.0")

        if max_weight > x_size:
            edge_widths.append(weight // x_size + 1)  
        else:
            edge_widths.append(weight) 

    nx.draw_networkx_edges(
        G, pos, edge_color=edge_colors, style="solid",
        arrowstyle="->", arrowsize=15, width=edge_widths,
        connectionstyle=edge_styles
    )

    # Dibujar etiquetas de los nodos
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="darkblue")

    # Añadir un título al grafo
    plt.title(f"Grafo de menciones en #{canal.name}, para {limit} mensajes", fontsize=16, fontweight="bold")

    # Guardar la imagen del grafo
    plt.savefig("grafo.png", bbox_inches="tight", dpi=300)
    plt.close()

    # Enviar la imagen al canal
    await ctx.send(file=discord.File("grafo.png"))  


# Reemplaza 'TU_TOKEN' con el token de tu bot
bot.run(config.TOKEN)