import discord
from discord.ext import commands, tasks
import time
import requests
import os
import holehe
import platform
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from discord import ui, Embed, SelectOption, Intents
import subprocess
import json
from requests.exceptions import HTTPError, SSLError, RequestException
import io
import logging
import base64
from datetime import datetime
import asyncio
import sys
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
import asyncio

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "YOUR_TOKEN"
CHANNEL_ID_BUMP = 1295786617428119664
CHANNEL_ID = 1328058756969402501
ROLE_ID = 1345067345911222443


intents = discord.Intents.all()  # Permissions pour l'accès aux événements du bot
bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

@tasks.loop(hours=5)  # Rappel toutes les 5 heures
async def bump_reminder():
    await bot.wait_until_ready()
    logger.info("bump_reminder est en cours d'exécution...")

    channel = bot.get_channel(CHANNEL_ID_BUMP)
    if channel:
        try:
            # Envoie du message de rappel
            await channel.send(f"<@&{ROLE_ID}> **N'oubliez pas de bump le serveur avec `/bump` !**")
            logger.info(f"Message de rappel envoyé avec succès dans le canal {CHANNEL_ID_BUMP}.")
        except discord.errors.Forbidden:
            logger.error(f"Erreur : Le bot n'a pas la permission d'envoyer des messages dans le canal {CHANNEL_ID_BUMP}.")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message dans le canal {CHANNEL_ID_BUMP}: {e}")
    else:
        logger.error(f"Erreur : Impossible de trouver le canal {CHANNEL_ID_BUMP}. Vérifie les permissions et l'ID.")

@bot.event
async def on_ready():
    logger.info(f"{bot.user} a bien été connecté !")
    await asyncio.sleep(1)

    # Vérifier si la tâche bump_reminder est déjà en cours, sinon on la démarre
    if not bump_reminder.is_running():
        bump_reminder.start()
        logger.info("La tâche bump_reminder a été démarrée !")
    else:
        logger.warning("La tâche bump_reminder était déjà en cours !")

    logger.info(f"Bot connecté comme {bot.user}")

    # Envoyer un message de bienvenue dans un canal spécifique
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            current_date = datetime.now().strftime("%d-%m-%Y")
            current_time = datetime.now().strftime("%H:%M:%S")
            # Envoi du message dans le canal
            await channel.send(f"**Bot connecté en tant que** `{bot.user.name}` **le** `{current_date}` **à** `{current_time}` **avec succès ! 🚀**")
            logger.info(f"Message de bienvenue envoyé avec succès dans le canal {CHANNEL_ID}.")
        except discord.errors.Forbidden:
            logger.error(f"Erreur : Le bot n'a pas la permission d'envoyer des messages dans le canal {CHANNEL_ID}.")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message de bienvenue dans le canal {CHANNEL_ID}: {e}")
    else:
        logger.error(f"Erreur : Impossible de trouver le canal {CHANNEL_ID}. Vérifie l'ID et les permissions.")


# Définition de la classe SeekApiClient
class SeekApiClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_documents(self, search_string, display_filename=True, size=1000):
        # Implémentation de la méthode search_documents
        # Cette méthode doit retourner les documents trouvés
        # Pour l'exemple, nous retournons une liste vide
        return []

@bot.command()
async def help(ctx):
    bot_latency = round(bot.latency * 1000)
    embed = Embed(
        title="Liste des Commandes",
        description="Choisissez une catégorie pour afficher les commandes disponibles.",
        color=0xFF0000
    )
    embed.add_field(
        name="Info du BOT :",
        value=f"Nombre de commandes : 16\nLatence : {bot_latency} ms\nPréfixe : +",
        inline=False
    )
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png"
    )
    embed.set_footer(text="Projet Searcher")

    options = [
        SelectOption(label="Accueil", description="Retour au menu d'accueil", emoji="🌎"),
        SelectOption(label="API", description="Commandes API", emoji="🔍"),
        SelectOption(label="Osint", description="Commandes dédiées à l'OSINT", emoji="🕵"),
        SelectOption(label="FiveM", description="Commandes dédiées à FiveM", emoji="🎮"),
    ]

    class HelpMenu(ui.Select):
        def __init__(self):
            super().__init__(placeholder="Sélectionnez une catégorie", options=options)

        async def callback(self, interaction):
            selected = self.values[0]
            if selected == "Accueil":
                await interaction.response.edit_message(embed=embed)
            elif selected == "API":
                embed_api = Embed(
                    title="Commandes API",
                    description="Voici les commandes disponibles :\n\n"
                                "**+naz** `<mot-clé>` : Recherche Avec l'API NazAPI.\n"
                                "**+snusbase** `<mot-clé>` : Recherche Avec l'API SnusBase.\n"
                                "**+leakcheck** `<e-mail>` : Recherche Avec Leakcheck.io.\n"
                                "**+email** `<email>` : Rechercher grâce à un E-mail.\n"
                                "**+github** `<pseudo>` : Rechercher grâce à un pseudo Github.\n"
                                "**+whois** `<domaine>` : Rechercer grâce à un Domaine.\n",
                    color=0xFF0000
                )
                await interaction.response.edit_message(embed=embed_api)
            elif selected == "Osint":
                embed_osint = Embed(
                    title="Commandes OSINT",
                    description="Voici les commandes disponibles :\n\n"
                                "**+ipinfo** `<IP>` : Scanner une adresse IP.\n"
                                "**+dork** `<mot-clés>` : Rechercher un mot-clés avec Google-Dork.\n"
                                "**+sherlock** `<pseudo>` : Rechercher un Pseudo sur un réseaux sociaux.\n"
                                "**+holehe** `<e-mail>` : Permet de savoir l'email est inscrit sur quelle sites.\n"
                                "**+steam** `<ID>` : Informations sur un Steam ID.\n"
                                "**+mc** `<pseudo>` : Informations sur un compte Minecraft.\n"
                                "**+userinfo** `<ID>` : Informations sur une ID discord.\n"
                                "**+redline** `<mail>` : Rechercher dans les redline.\n"
                                "**+phoneinfo** `<numéro>` : Informations sur un numéro de téléphone.\n"
                                "**+dnsinfo** `<nom de domaine>` : Informations DNS.\n"
                                "**+roblox** `<pseudo>` : Rechercher avec un pseudo Roblox.",
                    color=0xFF0000
                )
                await interaction.response.edit_message(embed=embed_osint)
            elif selected == "FiveM":
                embed_fivem = Embed(
                    title="Commandes FiveM",
                    description="Voici les commandes disponibles :\n\n"
                                "**+fivem** `<id/license>` : Recherche dans les Scraps FiveM.\n"
                                "**+scrap** `<cfx_code>` : Sert à Scrap un serveur FiveM.\n"
                                "**+fivemip** `<id/license>` : Recherche dans les DB !p.",
                    color=0xFF0000
                )
                await interaction.response.edit_message(embed=embed_fivem)

    class HelpView(ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(HelpMenu())

    await ctx.send(embed=embed, view=HelpView())

@bot.command()
async def dnsinfo(ctx, domain: str):
    if ctx.channel.id != 1328058756969402501: # ID du canal autorisé
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Projet Searcher")
        await ctx.send(embed=error_embed)
        return

    try:
        dns_data = {
            "Domaine": domain,
            "Adresse IP": "192.168.0.1",
            "Serveur NS": "ns1.example.com",
            "Pays": "France"
        }

        embed = discord.Embed(
            title="Informations DNS",
            description=f"Voici les informations pour le domaine **{domain}**.",
            color=0xFF0000
        )
        embed.add_field(name="Domaine", value=dns_data["Domaine"], inline=False)
        embed.add_field(name="Adresse IP", value=dns_data["Adresse IP"], inline=True)
        embed.add_field(name="Serveur NS", value=dns_data["Serveur NS"], inline=True)
        embed.add_field(name="Pays", value=dns_data["Pays"], inline=False)
        embed.set_footer(text="World-Bases")

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite lors de la recherche : {str(e)}")

@bot.command()
async def ipinfo(ctx, ip: str):
    if ctx.channel.id != 1328058756969402501: # ID du canal autorisé
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Projet Searcher")
        await ctx.send(embed=error_embed)
        return

    api_key = "vgms4ast2DCBdkEf5Klw0ufUlDC4V6tB"
    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if "ip" in data:
            embed = discord.Embed(
                title="🌐 Informations IP",
                description=f"Voici les informations pour l'adresse IP **{ip}**.",
                color=0xFF0000
            )
            embed.add_field(name="📍 IP", value=data.get("ip", "N/A"), inline=False)
            embed.add_field(name="🌍 Pays", value=data.get("country_name", "N/A"), inline=True)
            embed.add_field(name="🗺 Ville", value=data.get("city", "N/A"), inline=True)
            embed.add_field(name="🏢 Organisation", value=data.get("org", "N/A"), inline=False)
            embed.set_footer(text="World-Bases")

            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Aucune donnée trouvée pour cette IP.")
    except Exception as e:
        await ctx.send(f"❌ Une erreur s'est produite : {str(e)}")

@bot.command()
async def email(ctx, email: str):
    if ctx.channel.id != 1328058756969402501: # ID du canal autorisé
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Projet Searcher")
        await ctx.send(embed=error_embed)
        return

    api_key = "d813b0401193fd8ca1d1068971a152f8889151d9"
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if "data" in data:
            email_data = data["data"]

            embed = discord.Embed(
                title="Vérification E-mail",
                description=f"Voici les informations pour l'e-mail **{email}**.",
                color=0xFF0000
            )
            embed.add_field(name="E-mail", value=email_data.get("email", "N/A"), inline=False)
            embed.add_field(name="Valide", value="Oui" if email_data.get("result") == "deliverable" else "Non", inline=True)
            embed.add_field(name="Score de Confiance", value=email_data.get("score", "N/A"), inline=True)
            embed.set_footer(text="Recherche effectuée avec succès.")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucune donnée trouvée pour cet e-mail.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {str(e)}")

@bot.command(name="phoneinfo")
async def phoneinfo(ctx, phone: str):
    ALLOWED_CHANNEL_ID = 1328058756969402501 # ID du canal autorisé
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Projet Searcher")
        await ctx.send(embed=error_embed)
        return

    api_key = "b0e84f98f549f1ecf6364604bc9a415f"
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("valid"):
            embed = discord.Embed(
                title="📱 Informations Téléphone",
                description=f"Voici les informations pour le numéro **{phone}**.",
                color=0xFF0000
            )
            embed.add_field(name="Numéro", value=data.get("number", "N/A"), inline=False)
            embed.add_field(name="Code Pays", value=data.get("country_code", "N/A"), inline=True)
            embed.add_field(name="Pays", value=data.get("country_name", "N/A"), inline=True)
            embed.add_field(name="Localisation", value=data.get("location", "N/A"), inline=False)
            embed.add_field(name="Opérateur", value=data.get("carrier", "N/A"), inline=True)
            embed.add_field(name="Type", value=data.get("line_type", "N/A"), inline=True)
            embed.add_field(name="📱 **WhatsApp**", value=f"[Accéder au profil WhatsApp](https://wa.me/{phone})", inline=True)
            embed.add_field(name="💬 **Telegram**", value=f"[Accéder au profil Telegram](https://t.me/{phone})", inline=True)
            embed.set_footer(text="#Projet Searcher")

            try:
                await ctx.author.send(embed=embed)
                info_embed = discord.Embed(
                    title="Résultat trouvé 🔎, vérifiez vos DMs !",
                    description="**⚠️ Vérifiez d'avoir activé vos messages privés !**.",
                    color=0xFF0000
                )
                info_embed.set_image(
                    url="https://cdn.discordapp.com/attachments/1313886334296789083/1315327224739532851/wldb_banner.png"
                )
                await ctx.send(embed=info_embed)
            except discord.Forbidden:
                dm_error_embed = discord.Embed(
                    title="Erreur d'envoi en MP",
                    description="Vos messages privés sont désactivés. Activez-les pour recevoir les résultats.",
                    color=0xFF0000
                )
                await ctx.send(embed=dm_error_embed)
        else:
            invalid_embed = discord.Embed(
                title="Numéro invalide",
                description=f"Le numéro **{phone}** est invalide ou aucune donnée n'a été trouvée.",
                color=0xFF0000
            )
            invalid_embed.set_footer(text="Projet Searcher")
            await ctx.send(embed=invalid_embed)

    except requests.exceptions.RequestException as req_err:
        error_embed = discord.Embed(
            title="Erreur API",
            description="Une erreur s'est produite lors de la connexion à l'API NumVerify.",
            color=0xFF0000
        )
        error_embed.add_field(name="Détails de l'erreur", value=str(req_err), inline=False)
        error_embed.set_footer(text="Vérifiez votre connexion ou votre clé API.")
        await ctx.send(embed=error_embed)

    except Exception as e:
        general_error_embed = discord.Embed(
            title="Erreur inconnue",
            description="Une erreur inattendue s'est produite.",
            color=0xFF0000
        )
        general_error_embed.add_field(name="Détails de l'erreur", value=str(e), inline=False)
        general_error_embed.set_footer(text="Contactez l'administrateur si le problème persiste.")
        await ctx.send(embed=general_error_embed)

@bot.command()
async def whois(ctx, domain: str):
    """
    Récupère les informations WHOIS d'un domaine via l'API WhoisXML.
    """
    api_key = "at_18VrQY0C9IgUWReyVJw8ybyZBb7oJ"
    url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={domain}&outputFormat=JSON"

    try:
        response = requests.get(url)
        data = response.json()

        if "WhoisRecord" in data:
            whois_data = data["WhoisRecord"]

            embed = discord.Embed(
                title="Informations WHOIS",
                description=f"Voici les informations pour le domaine **{domain}**.",
                color=0xFF0000
            )
            embed.add_field(name="Domaine", value=whois_data.get("domainName", "N/A"), inline=False)
            embed.add_field(name="Créé le", value=whois_data.get("createdDate", "N/A"), inline=True)
            embed.add_field(name="Expire le", value=whois_data.get("expiresDate", "N/A"), inline=True)
            embed.add_field(name="Organisation", value=whois_data.get("registrant", {}).get("organization", "N/A"), inline=False)
            embed.set_footer(text="Données extraites avec succès.")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucune donnée trouvée pour ce domaine.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {str(e)}")

@bot.command()
async def subdomains(ctx, domain: str):
    """
    Recherche des sous-domaines via l'API SecurityTrails.
    """
    api_key = "3qicABB3Uhud-lnxKWcFrq5sQuqTItD8"
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {"APIKEY": api_key}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if "subdomains" in data:
            subdomains = data["subdomains"]
            subdomains_list = "\n".join([f"{sub}.{domain}" for sub in subdomains[:20]])

            embed = discord.Embed(
                title="📁 Sous-domaines",
                description=f"Voici une liste de sous-domaines pour **{domain}**:",
                color=0xFF0000
            )
            embed.add_field(name="Sous-domaines", value=subdomains_list or "Aucun sous-domaine trouvé.", inline=False)
            embed.set_footer(text="World-Bases")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucun sous-domaine trouvé pour ce domaine.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {str(e)}")

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '_', filename)

@bot.command()
async def naz(ctx, *, request: str):
    """
    Recherche via l'API NazAPI et envoie les résultats dans un fichier.
    """
    try:
        api_key = "1501479747:EOHy2bG"
        url = "https://leakosintapi.com/"
        download_path = "./resultat/"

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        sanitized_request = sanitize_filename(request)
        file_path = os.path.join(download_path, f"leak2internet.txt")

        data = {
            "token": api_key,
            "request": request,
            "limit": 75,
            "lang": "fr"
        }

        response = requests.post(url, json=data)
        response_json = response.json()

        if "List" not in response_json:
            await ctx.send("❌ **Erreur**: Aucun résultat trouvé !")
            return

        list_data = response_json["List"]

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("──── Résultats NazAPI ────\n\n")
            for category, category_data in list_data.items():
                file.write(f"»»————- ★ {category} ★ ————-««\n")
                if "Data" not in category_data or not category_data["Data"]:
                    file.write("Aucun résultat dans cette catégorie.\n")
                    continue

                for data_item in category_data["Data"]:
                    if isinstance(data_item, dict):
                        for key, value in data_item.items():
                            file.write(f"{key}: {value}\n")
                    else:
                        file.write("Format de données inattendu.\n")
                file.write("\n")

        embed = discord.Embed(
            title="Résultat envoyé en MP ! <a:GMD_Animated_Red_Verified:1314259390592843826>",
            description="Regarde tes MP pour les résultats de ta recherche.",
            color=0xFF0000
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=675305bb&is=6751b43b&hm=925fd364b427b14527297e3b0c1c068cea8b35eae0ddae9aed3553735d1b871f&")
        await ctx.send(embed=embed)

        await ctx.author.send(file=discord.File(file_path))

    except Exception as e:
        await ctx.send(f"❌ Une erreur s'est produite : {str(e)}")

ALLOWED_CHANNEL_ID = 1328058756969402501 # ID du canal autorisé

@bot.command()
async def fivem(ctx, *, keyword):
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        embed_error = discord.Embed(
            title="__Erreur__",
            description=f"Cette commande ne peut être utilisée que dans le salon : <#{ALLOWED_CHANNEL_ID}>",
            color=0xFF0000
        )
        embed_error.set_footer(text=".gg/kkuU6CbQBG")
        await ctx.send(embed=embed_error)
        return

    embed_loading = discord.Embed(
        description=f"**Recherche en cours pour :** `{keyword}` <a:xans_search:1284531451391508611>",
        color=0xFF0000
    )
    search_message = await ctx.send(embed=embed_loading)

    db_folder = "dump"
    results = []

    ascii_art = r"""
   _____                     _     ______ _____  
  / ____|                   | |   |  ____|  __ \ 
 | (___   ___  __ _ _ __ ___| |__ | |__  | |__) | .gg/kkuU6CbQBG
  \___ \ / _ \/ _` | '__/ __| '_ \|  __| |  _  / 
  ____) |  __/ (_| | | | (__| | | | |    | | \ \ 
 |_____/ \___|\__,_|_|  \___|_| |_|_|    |_|  \_\
                                                 
    """

    for filename in os.listdir(db_folder):
        file_path = os.path.join(db_folder, filename)

        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if keyword.lower() in line.lower():
                        results.append(line.strip())

    if results:
        results_filename = "leak2internet.txt"
        with open(results_filename, 'w', encoding='utf-8') as f:
            f.write(ascii_art + "\n\n")
            f.write('\n'.join(results))

        await ctx.author.send(file=discord.File(results_filename))
        os.remove(results_filename)

        embed = discord.Embed(
            title="Résultat trouvé 🔎, vérifiez vos DMs !",
            description="**⚠️ Vérifiez d'avoir activé vos messages privés !**.",
            color=0xFF0000
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=675305bb&is=6751b43b&hm=925fd364b427b14527297e3b0c1c068cea8b35eae0ddae9aed3553735d1b871f&")  # Lien de l'image
        await search_message.edit(embed=embed)

    else:
        embed_no_result = discord.Embed(
            title="<:x_red_verified:1314259356178714624> Aucun résultat trouvé <:x_red_verified:1314259356178714624>",
            description=f"Impossible de trouver un résultat pour : **{keyword}**\n\n"
                        "Vérifiez les détails suivants :\n\n"
                        "Assurez-vous que l'ID Discord est correct.\n"
                        "Assurez-vous que l'utilisateur joue à FiveM.",
            color=0xFF0000
        )
        embed_no_result.set_footer(text="World-Bases")
        await ctx.send(embed=embed_no_result)

ALLOWED_CHANNEL_ID = 11328058756969402501 # ID du canal autorisé

@bot.command()
async def fivemip(ctx, *, keyword):
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        embed_error = discord.Embed(
            title="__Erreur__",
            description=f"Cette commande ne peut être utilisée que dans le salon : <#{ALLOWED_CHANNEL_ID}>",
            color=0xFF0000
        )
        embed_error.set_footer(text="World-Bases")
        await ctx.send(embed=embed_error)
        return

    embed_loading = discord.Embed(
        description=f"**Recherche en cours pour :** `{keyword}` <a:xans_search:1284531451391508611>",
        color=0xFF0000
    )
    search_message = await ctx.send(embed=embed_loading)

    db_folder = "db"
    results = []

    ascii_art = r"""
   _____                     _     ______ _____  
  / ____|                   | |   |  ____|  __ \ 
 | (___   ___  __ _ _ __ ___| |__ | |__  | |__) |
  \___ \ / _ \/ _` | '__/ __| '_ \|  __| |  _  / 
  ____) |  __/ (_| | | | (__| | | | |    | | \ \  .gg/kkuU6CbQBG
 |_____/ \___|\__,_|_|  \___|_| |_|_|    |_|  \_\
                                                 
    """

    for filename in os.listdir(db_folder):
        file_path = os.path.join(db_folder, filename)

        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if keyword.lower() in line.lower():
                        results.append(line.strip())

    if results:
        results_folder = ".gg"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        results_filename = os.path.join(results_folder, "leak2internet.txt")
        with open(results_filename, 'w', encoding='utf-8') as f:
            f.write(ascii_art + "\n\n")
            f.write('\n'.join(results))

        await ctx.author.send(file=discord.File(results_filename))
        os.remove(results_filename)

        embed = discord.Embed(
            title="Résultat trouvé 🔎, vérifiez vos DMs !",
            description="**⚠️ Vérifiez d'avoir activé vos messages privés !**",
            color=0xFF0000
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=675305bb&is=6751b43b&hm=925fd364b427b14527297e3b0c1c068cea8b35eae0ddae9aed3553735d1b871f&")
        await search_message.edit(embed=embed)

    else:
        embed_no_result = discord.Embed(
            title="<:x_red_verified:1314259356178714624> Aucun résultat trouvé <:x_red_verified:1314259356178714624>",
            description=f"Impossible de trouver un résultat pour : **{keyword}**\n\n"
                        "Vérifiez les détails suivants :\n\n"
                        "Assurez-vous que l'ID Discord est correct.\n"
                        "Assurez-vous que l'utilisateur joue à FiveM.",
            color=0xFF0000
        )
        embed_no_result.set_footer(text="World-Bases")
        await ctx.send(embed=embed_no_result)

STEAM_API_KEY = 'C8EE0D8E8D3FD87A88240A6A9C16F9D9'  # Steam-KEY
DEFAULT_AVATAR_URL = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/default_avatar.jpg"

@bot.command()
async def steam(ctx, steam_id: str):
    if ctx.channel.id != 1328058756969402501:
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Projet Searcher")
        await ctx.send(embed=error_embed)
        return

    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
    response = requests.get(url)
    data = response.json()

    if 'response' in data and 'players' in data['response'] and data['response']['players']:
        player = data['response']['players'][0]

        pseudo = player.get("personaname", "❌")
        profile_url = player.get("profileurl", "❌")
        country = player.get("loccountrycode", "❌")
        last_logoff = player.get("lastlogoff", "❌")
        status_code = player.get("personastate", 0)
        real_name = player.get("realname", "❌")
        avatar_url = player.get("avatarfull", DEFAULT_AVATAR_URL)

        status_map = {
            0: "Hors ligne",
            1: "En ligne",
            2: "Occupé",
            3: "Absent",
            4: "Sommeil",
            5: "Cherche du jeu",
            6: "En jeu"
        }
        status = status_map.get(status_code, "❌")

        if last_logoff != "❌":
            last_logoff = datetime.utcfromtimestamp(last_logoff).strftime('%Y-%m-%d %H:%M:%S UTC')
        else:
            last_logoff = "❌"

        if not avatar_url:
            avatar_url = DEFAULT_AVATAR_URL

        embed = discord.Embed(title="__Résultats :__", color=0x000000)
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Pseudo", value=pseudo, inline=False)
        embed.add_field(name="Profil", value=profile_url, inline=False)
        embed.add_field(name="Pays", value=country, inline=False)
        embed.add_field(name="Dernière connexion", value=last_logoff, inline=False)
        embed.add_field(name="Statut", value=status, inline=False)
        embed.add_field(name="Nom complet", value=real_name, inline=False)

        await ctx.author.send(embed=embed)

        confirmation_embed = discord.Embed(
            title="Résultat trouvé 🔎, vérifiez vos DMs !",
            description="**⚠️ Vérifiez d'avoir activé vos messages privés !**",
            color=0xFF0000
        )
        confirmation_embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=675305bb&is=6751b43b&hm=925fd364b427b14527297e3b0c1c068cea8b35eae0ddae9aed3553735d1b871f&")  # Ajout de l'image
        await ctx.send(embed=confirmation_embed)
    else:
        error_embed = discord.Embed(
            title="__Erreur__ ",
            description=f"<:x_red_verified:1314259356178714624> Aucune information trouvée pour l'ID Steam : `{steam_id}`.\n <:x_red_verified:1314259356178714624> Verifier que l'ID Steam est correct.",
            color=0xFF0000
        )
        error_embed.set_footer(text="© SearchFR")
        await ctx.send(embed=error_embed)

GITHUB_TOKEN = os.getenv('kzjbOg3iOm4k4MRpBss76yxIZSPJtoOPaqxirsfX')  # Github-KEY
EMBED_COLOR = 0xFF0000

@bot.command(name='github')
async def github(ctx, username: str):
    if ctx.channel.id != 1328058756969402501:
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=EMBED_COLOR
        )
        error_embed.set_footer(text="Projet SearchFR")
        await ctx.send(embed=error_embed)
        return

    headers = {}
    if GITHUB_TOKEN:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        embed = discord.Embed(
            title=f"Profil GitHub de {data['login']}",
            description=data.get('bio', 'Aucune bio disponible.'),
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=data['avatar_url'])
        embed.set_author(name="GitHub",
        icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.set_footer(text="SearchFR")
        embed.add_field(name="Nom", value=data.get('name', 'Non spécifié'), inline=True)
        embed.add_field(name="Localisation", value=data.get('location', 'Non spécifiée'), inline=True)
        embed.add_field(name="Public Repos", value=str(data['public_repos']), inline=True)
        embed.add_field(name="Public Gists", value=str(data['public_gists']), inline=True)
        embed.add_field(name="Followers", value=str(data['followers']), inline=True)
        embed.add_field(name="Following", value=str(data['following']), inline=True)
        embed.add_field(name="Type d'utilisateur", value=data['type'], inline=True)
        embed.add_field(name="Créé le", value=data['created_at'], inline=True)
        embed.add_field(name="Dernière mise à jour", value=data['updated_at'], inline=True)
        if data.get('company'):
            embed.add_field(name="Entreprise", value=data['company'], inline=True)
        if data.get('email'):
            embed.add_field(name="Email", value=data['email'], inline=False)
        else:
            embed.add_field(name="Email", value="Non spécifié ou privé.", inline=False)
        if data.get('twitter_username'):
            embed.add_field(name="Twitter",
            value=f"[{data['twitter_username']}](https://twitter.com/{data['twitter_username']})", inline=False)
        embed.add_field(name="Profil GitHub", value=f"[Voir le profil]({data['html_url']})", inline=False)
        if data.get('blog'):
            embed.add_field(name="Blog", value=data['blog'], inline=False)

        try:
            await ctx.author.send(embed=embed)

            notify_embed = discord.Embed(
                title="Résultat trouvé 🔎, vérifiez vos DMs !",
                description="**⚠️ Vérifiez d'avoir activé vos messages privés !**",
                color=EMBED_COLOR
            )
            notify_embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=675305bb&is=6751b43b&hm=925fd364b427b14527297e3b0c1c068cea8b35eae0ddae9aed3553735d1b871f&")  # Ajout de l'image
            notify_embed.set_footer(text="SearchFR")
            await ctx.send(embed=notify_embed)

        except discord.Forbidden:
            await ctx.send("Je ne peux pas envoyer de message privé. Vérifie tes paramètres de confidentialité.")
    else:
        error_embed = discord.Embed(
            title="Erreur",
            description="Utilisateur GitHub non trouvé.",
            color=EMBED_COLOR
        )
        error_embed.set_footer(text="© Projet")
        await ctx.send(embed=error_embed)

def google_dork_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a')
        if title and link:
            results.append(f"{title.text}\n{link['href']}")

    return results

@bot.command()
async def dork(ctx, *, keyword):
    if ctx.channel.id != 1328058756969402501:
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Projet Searcher")
        await ctx.send(embed=error_embed)
        return

    results = google_dork_search(keyword)

    if results:
        await ctx.author.send("\n\n".join(results))

        embed = discord.Embed(
            title="Résultat trouvé 🔎, vérifiez vos DMs !",
            description="**⚠️ Vérifiez d'avoir activé vos messages privés !**",
            color=0xFF0000
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=675305bb&is=6751b43b&hm=925fd364b427b14527297e3b0c1c068cea8b35eae0ddae9aed3553735d1b871f&")  # Image ajoutée ici
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description="<:x_red_verified:1314259356178714624> Aucun résultat trouvé pour ce mot-clé.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)

ROBLOX_API_URL = "https://users.roblox.com/v1/users"
BADGES_API_URL = "https://badges.roblox.com/v1/users"
STATUS_API_URL = "https://users.roblox.com/v1/users/{}/status"
FRIENDS_API_URL = "https://friends.roblox.com/v1/users/{}/friends/count"
AVATAR_API_URL = "https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png"

@bot.command()
async def roblox(ctx, username: str):
    if ctx.channel.id != 1328058756969402501:
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être exécutée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Projet Searcher")
        await ctx.send(embed=error_embed)
        return

    search_url = "https://users.roblox.com/v1/usernames/users"
    payload = {
        "usernames": [username],
        "excludeBannedUsers": False
    }

    try:
        search_response = requests.post(search_url, json=payload)

        if search_response.status_code == 200:
            search_data = search_response.json()

            if "data" in search_data and len(search_data["data"]) > 0:
                user_info = search_data["data"][0]
                user_id = user_info.get("id")
                display_name = user_info.get("displayName", "Inconnu")
                account_name = user_info.get("name", "Inconnu")

                user_url = f"{ROBLOX_API_URL}/{user_id}"
                user_response = requests.get(user_url)

                if user_response.status_code == 200:
                    user_details = user_response.json()
                    creation_date = user_details.get("created", "Inconnu")

                    badges_url = f"{BADGES_API_URL}/{user_id}/badges"
                    badges_response = requests.get(badges_url)
                    badges = "Aucun badge trouvé"
                    if badges_response.status_code == 200:
                        badges_data = badges_response.json().get("data", [])
                        badges = ", ".join([badge["name"] for badge in badges_data[:5]]) or "Aucun badge"

                    status_url = STATUS_API_URL.format(user_id)
                    status_response = requests.get(status_url)
                    user_status = status_response.json().get("status", "Aucun statut") if status_response.status_code == 200 else "Inconnu"

                    friends_url = FRIENDS_API_URL.format(user_id)
                    friends_response = requests.get(friends_url)
                    friend_count = friends_response.json().get("count", "Inconnu") if friends_response.status_code == 200 else "Inconnu"

                    avatar_url = AVATAR_API_URL.format(user_id=user_id)
                    avatar_response = requests.get(avatar_url)
                    avatar_data = avatar_response.json().get("data", [])
                    avatar_image = avatar_data[0]["imageUrl"] if avatar_data else None

                    embed = discord.Embed(
                        title=f"Informations Roblox pour {account_name}",
                        color=0xFF0000
                    )
                    embed.add_field(name="Nom d'utilisateur", value=account_name, inline=False)
                    embed.add_field(name="Nom affiché", value=display_name, inline=False)
                    embed.add_field(name="ID utilisateur", value=user_id, inline=False)
                    embed.add_field(name="Date de création", value=creation_date, inline=False)
                    embed.add_field(name="Badges", value=badges, inline=False)
                    embed.add_field(name="Statut", value=user_status, inline=False)
                    embed.add_field(name="Nombre d'amis", value=friend_count, inline=False)
                    if avatar_image:
                        embed.set_thumbnail(url=avatar_image)
                    embed.set_footer(text="© Leak-Internet")

                    # Envoi en MP
                    try:
                        await ctx.author.send(embed=embed)

                        confirm_embed = discord.Embed(
                            title="Résultat trouvé 🔎, vérifiez vos DMs !",
                            description="**⚠️ Vérifiez d'avoir activé vos messages privés !**",
                            color=0xFF0000
                        )
                        confirm_embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png")
                        await ctx.send(embed=confirm_embed)

                    except discord.Forbidden:
                        await ctx.send("Je ne peux pas envoyer de message privé. Vérifie tes paramètres de confidentialité.")
                else:
                    await ctx.send("<:x_red_verified:1314259356178714624> Impossible de récupérer les détails de l'utilisateur Roblox.")
            else:
                await ctx.send(f"<:x_red_verified:1314259356178714624> Aucun utilisateur trouvé pour le nom d'utilisateur : {username}")
        else:
            await ctx.send("Erreur lors de la recherche de l'utilisateur.")
    except Exception as e:
        await ctx.send(f"Une erreur est survenue : {e}")

SNUSBASE_API_KEY = 'sb6sffauk36ll3n9ysf05f5vxwkcr'
SNUSBASE_API_URL = 'https://api.snusbase.com/data/search'

@bot.command(name='snusbase')
async def snusbase(ctx, *, terms: str):
    """Recherche dans l'API Snusbase et envoie les résultats en DM."""

    allowed_channel_id = 1328058756969402501 # ID du canal autorisé
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("Cette commande peut être utilisée que dans le bon channel.")
        return

    search_embed = discord.Embed(
        description="**Recherche en cours, merci de patienter...**",
        color=0xFF0000
    )
    search_message = await ctx.send(embed=search_embed)

    terms_list = terms.split()
    payload = {
        "terms": terms_list,
        "types": ["username", "email", "lastip", "password", "hash", "name"]
    }

    headers = {
        'Auth': SNUSBASE_API_KEY,
        'Content-Type': 'application/json',
    }

    ascii_header = """\


#.gg/kkuU6CbQBG
                         
                        discord.gg/kkuU6CbQBG                           

"""

    try:
        response = requests.post(SNUSBASE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        results_filename = 'leak2internet.txt'

        with open(results_filename, 'w', encoding='utf-8') as file:
            file.write(ascii_header)
            file.write("\n")

            for db_name, entries in data['results'].items():
                file.write(f"»»————- ★ Trouvée dans : {db_name} ★ ————-««\n\n")
                for entry in entries:
                    formatted_entry = "\n".join(f"{key}: {value}" for key, value in entry.items())
                    file.write(formatted_entry)
                    file.write("\n\n")

        await ctx.author.send(file=discord.File(results_filename))

        results_embed = discord.Embed(
            title="Résultat trouvé 🔎, vérifiez vos DMs !",
            description="**⚠️ Vérifiez d'avoir activé vos messages privés !**",
            color=0xFF0000
        )
        results_embed.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=675305bb&is=6751b43b&hm=925fd364b427b14527297e3b0c1c068cea8b35eae0ddae9aed3553735d1b871f&")
        await search_message.delete()
        await ctx.send(embed=results_embed)

    except requests.exceptions.HTTPError as http_err:
        await ctx.send(f"Erreur lors de la requête API : {http_err}")
    except Exception as err:
        await ctx.send(f"Une erreur s'est produite : {err}")

HUDSONROCK_API_KEY = "ROCKHUDSONROCK"

def hudsonrock_lookup(endpoint, query_param, query_value):
    try:
        result = subprocess.run(
            [
                "curl",
                "-X", "GET",
                f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/{endpoint}",
                "-H", f"api-key: {HUDSONROCK_API_KEY}",
                "-G",
                "--data-urlencode", f"{query_param}={query_value}",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return f"Erreur lors de l'exécution de la commande curl : {result.stderr}"

        data = json.loads(result.stdout)

        embed = discord.Embed(
            title="Résultat trouvé 🔎",
            description=f"Voici les résultats pour : {query_value}",
            color=0xFF0000
        )

        field_count = 0
        for steal in data.get("stealers", []):
            if field_count >= 25:
                break
            embed.add_field(name="📝 **Nom de l'ordinateur**", value=f"``{steal.get('computer_name', 'Inconnu')}``", inline=True)
            field_count += 1
            embed.add_field(name="🖥 **Système d'exploitation**", value=f"``{steal.get('operating_system', 'Inconnu')}``", inline=True)
            field_count += 1
            embed.add_field(name="🔒 **IP**", value=f"``{steal.get('ip', 'Inconnue')}``", inline=True)
            field_count += 1
            embed.add_field(name="📅 **Date de compromission**", value=f"``{steal.get('date_compromised', 'Inconnue')}``", inline=True)
            field_count += 1
            embed.add_field(name="🔰 **Services compromis**", value=f"``{steal.get('total_user_services', 'Inconnu')}``", inline=True)
            field_count += 1
            embed.add_field(name="🛡 **Anti-virus utilisé**", value=f"``{', '.join(steal.get('antiviruses', ['Aucun']))}``", inline=False)
            field_count += 1

        return embed

    except json.JSONDecodeError:
        return "Erreur : les données reçues ne sont pas valides JSON."
    except subprocess.CalledProcessError:
        return "Erreur lors de la commande curl."
    except Exception as e:
        return f"Erreur de récupération des informations pour {query_value} : {e}"

def determine_query_type(query_value):
    if re.match(r"[^@]+@[^@]+\.[^@]+", query_value):
        return "search-by-email", "email"
    elif re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", query_value):
        return "search-by-ip", "ip"
    else:
        return None, None

@bot.command(name="redline")
async def redline(ctx, query: str):
    ALLOWED_CHANNEL_ID = 1328058756969402501 # ID du canal autorisé
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(embed=discord.Embed(
            title="Erreur",
            description="❌ Vous ne pouvez pas utiliser cette commande dans ce salon. Commande disponible ici : <#1314285291225481231>",
            color=0xFF0000
        ))
        return

    endpoint, query_param = determine_query_type(query)
    if not endpoint or not query_param:
        await ctx.send(embed=discord.Embed(
            title="Format invalide",
            description="❌ Veuillez entrer une **adresse email** ou une **adresse IP** valide.",
            color=0xFF0000
        ))
        return

    result = hudsonrock_lookup(endpoint, query_param, query)

    if isinstance(result, discord.Embed):
        try:
            await ctx.author.send(embed=result)

            confirmation_embed = discord.Embed(
                title="Résultat trouvé 🔎, vérifiez vos DMs !",
                description="⚠️ Vérifiez d'avoir activé vos messages privés !",
                color=0xFF0000
            )
            confirmation_embed.set_image(url="https://cdn.discordapp.com/attachments/1313886334296789083/1315327224739532851/wldb_banner.png?ex=6757016f&is=6755afef&hm=cb788c4472a80bf9a8e986142db549584d0e5b6e1dcd56be61750be3e95b9eab&")
            confirmation_embed.set_footer(text="#Projet")

            await ctx.send(embed=confirmation_embed)
        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                title="Erreur",
                description="❌ Impossible d'envoyer un message privé. Activez vos messages privés.",
                color=0xFF0000
            ))
    else:
        await ctx.send(embed=discord.Embed(
            title="Erreur lors de la recherche",
            description=result,
            color=0xFF0000
        ))

AUTHORIZED_CHANNEL_ID = 1314285291225481231
LEAKCHECK_URL = "https://leakcheck.net/api/public?key=49535f49545f5245414c4c595f4150495f4b4559&check={}"

@bot.command(name="leakcheck")
async def leakcheck(ctx, email: str):
    if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
        embed = discord.Embed(
            title="Erreur",
            description=f"Commande disponible uniquement ici : <#{AUTHORIZED_CHANNEL_ID}>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    await ctx.send(embed=discord.Embed(
        title="Recherche en cours...",
        description="*Veuillez patienter pendant que je rassemble les informations...*",
        color=0xFF0000
    ).set_footer(text="Recherche en cours..."))

    data = fetch_leakcheck_data(email)
    result = format_leakcheck_result(data, email)

    if isinstance(result, discord.File):
        await ctx.author.send(file=result)
    else:
        await ctx.author.send(result)

    await ctx.send(embed=discord.Embed(
        title=f"Résultats trouvés pour `{email}` !",
        description="⚠️ **Vérifiez vos messages privés !** Les résultats ont été envoyés en DM.",
        color=0xFF0000
    ).set_image(url="https://cdn.discordapp.com/attachments/1313886334296789083/1314336891033878528/wldb_banner.png").set_footer(text="Recherche terminée."))

def fetch_leakcheck_data(query):
    try:
        response = requests.get(LEAKCHECK_URL.format(query))
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def format_leakcheck_result(data, email):
    if data and data.get("success"):
        found = data.get("found", 0)
        passwords = data.get("passwords", 0)
        sources = data.get("sources", [])

        if len(sources) > 25 or any(len(f"- {source.get('name', 'Inconnu')} (Date: {source.get('date', 'Inconnue')})") > 1024 for source in sources):
            file_content = f"Résultats pour : {email}\nFuites trouvées: {found}\nMots de passe compromis: {passwords}\nSources:\n"
            file_content += "\n".join([f"- {source.get('name', 'Inconnu')} (Date: {source.get('date', 'Inconnue')})" for source in sources])
            file_output = io.StringIO(file_content)
            return discord.File(file_output, filename="results.txt")

        text_content = f"Résultats pour `{email}` :\nFuites : {found}\nMots de passe compromis : {passwords}\nSources :\n"
        text_content += "\n".join([f"- {source.get('name', 'Inconnu')} (Date: {source.get('date', 'Inconnue')})" for source in sources])
        return text_content
    else:
        return f"Aucune fuite trouvée pour `{email}` dans **LeakCheck**."

ALLOWED_CHANNEL_ID = 1328058756969402501 # ID du canal autorisé
scrape_data = {}

async def get_server_info(server_id):
    url = f'https://servers-frontend.fivem.net/api/servers/single/{server_id}'
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random,
        'method': 'GET'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            server_data = response.json()
            return server_data, None
        else:
            return None, f"Erreur : L'API a renvoyé un statut {response.status_code}."
    except Exception as e:
        return None, f"Erreur: {str(e)}"

def create_player_embed(server_code, players, page_num):
    total_pages = (len(players) - 1) // 10 + 1
    start_index = page_num * 10
    end_index = start_index + 10
    embed = discord.Embed(
        title=f"Résultats pour le serveur `{server_code}` (Page {page_num + 1}/{total_pages})",
        color=0xFF0000
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1313886334296789083/1314336891033878528/wldb_banner.png")

    for player in players[start_index:end_index]:
        name = player.get('name', 'Inconnu')
        identifiers = player.get('identifiers', ['Aucun identifiant trouvé'])
        identifiers_str = "\n".join(identifiers)
        embed.add_field(name=f"Joueur : {name}", value=f"Identifiants :\n{identifiers_str}", inline=False)

    return embed

async def send_player_page(ctx_or_interaction, page_num):
    user = ctx_or_interaction.user if isinstance(ctx_or_interaction, discord.Interaction) else ctx_or_interaction.author
    user_id = user.id
    players = scrape_data[user_id]['players']
    server_code = scrape_data[user_id]['server_code']

    embed = create_player_embed(server_code, players, page_num)

    view = ui.View()
    if page_num > 0:
        view.add_item(ui.Button(emoji="⬅️", style=discord.ButtonStyle.primary, custom_id="prev_page"))
    if page_num < (len(players) - 1) // 10:
        view.add_item(ui.Button(emoji="➡️", style=discord.ButtonStyle.primary, custom_id="next_page"))
    view.add_item(ui.Button(emoji="📥", style=discord.ButtonStyle.success, custom_id="download_json"))

    if scrape_data[user_id]['current_msg']:
        await scrape_data[user_id]['current_msg'].edit(embed=embed, view=view)
    else:
        msg = await user.send(embed=embed, view=view)
        scrape_data[user_id]['current_msg'] = msg

    scrape_data[user_id]['current_page'] = page_num

@bot.command()
async def scrap(ctx, server_code):
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        error_embed = discord.Embed(
            title="Erreur",
            description=f"Commande disponible uniquement dans le salon <#{ALLOWED_CHANNEL_ID}>.",
            color=0xFF0000
        )
        await ctx.send(embed=error_embed)
        return

    embed = discord.Embed(
        title="Résultat trouvé 🔎, vérifiez vos DMs !",
        description="⚠️ Vérifiez d'avoir activé vos messages privés !",
        color=0xFF0000
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1313886334296789083/1314336891033878528/wldb_banner.png")
    embed.set_footer(text="© XX")
    await ctx.send(embed=embed)

    await ctx.author.send(f"Voici les résultats pour : `{server_code}`...")

    server_data, error_message = await get_server_info(server_code)

    if error_message:
        await ctx.author.send(f"Erreur : {error_message}")
        return

    if server_data:
        players = server_data['Data'].get('players', [])
        if not players:
            await ctx.author.send(f"Aucun joueur trouvé sur le serveur `{server_code}`.")
            return

        scrape_data[ctx.author.id] = {
            'players': players,
            'server_code': server_code,
            'current_page': 0,
            'current_msg': None
        }

        await send_player_page(ctx, 0)
    else:
        await ctx.author.send(f"Impossible de récupérer les données du serveur `{server_code}`.")

@bot.event
async def on_interaction(interaction):
    user_id = interaction.user.id
    if user_id not in scrape_data:
        return

    if interaction.data['custom_id'] == 'prev_page':
        current_page = scrape_data[user_id]['current_page']
        await send_player_page(interaction, current_page - 1)
        await interaction.response.defer()
    elif interaction.data['custom_id'] == 'next_page':
        current_page = scrape_data[user_id]['current_page']
        await send_player_page(interaction, current_page + 1)
        await interaction.response.defer()
    elif interaction.data['custom_id'] == 'download_json':
        players = scrape_data[user_id]['players']
        json_data = json.dumps(players, indent=4)
        file_name = f"{scrape_data[user_id]['server_code']}_players.json"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(json_data)
        await interaction.user.send(file=discord.File(file_name))
        await interaction.response.defer()

@bot.command()
async def holehe(ctx, email: str):
    channel_id = 1328058756969402501  # Assurez-vous que cet ID est correct
    if ctx.channel.id != channel_id:
        embed_error = discord.Embed(
            title="❌ Commande non autorisée",
            description="Vous ne pouvez pas utiliser cette commande ici.",
            color=0xFF0000
        )
        await ctx.send(embed=embed_error)
        return

    embed_loading = discord.Embed(
        title="Recherche en cours 🔎",
        description=f"Recherche des sites associés à l'email `{email}`...",
        color=0xFF0000
    )
    message = await ctx.send(embed=embed_loading)

    try:
        result = subprocess.run(["holehe", email], capture_output=True, text=True, check=True)

        formatted_result = result.stdout.strip() if result.stdout else "Aucun résultat trouvé."

        embed_result = discord.Embed(
            title="Résultat trouvé 🔎",
            description=f"Voici les résultats pour l'email `{email}` :\n\n```\n{formatted_result}\n```",
            color=0xFF0000
        )
        embed_result.set_footer(text="⚠️ Vérifiez d'avoir activé vos messages privés !")
        embed_result.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png")

        try:
            await ctx.author.send(embed=embed_result)
            embed_done = discord.Embed(
                title="Résultat trouvé 🔎, vérifiez vos DMs !",
                description="**⚠️ Vérifiez d'avoir activé vos messages privés !**",
                color=0xFF0000
            )
            embed_done.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png")  # Image ajoutée ici
            await message.edit(embed=embed_done)
        except discord.Forbidden:
            await message.edit(embed=discord.Embed(
                title="Erreur ❌",
                description="Impossible d'envoyer le résultat en DM. Vérifiez vos paramètres de confidentialité.",
                color=0xFF0000
            ))

    except subprocess.CalledProcessError as e:
        error_message = e.output if e.output else "Erreur inconnue lors de l'exécution."
        embed_error = discord.Embed(
            title="Erreur 🚨",
            description=f"Une erreur est survenue lors de l'exécution de Holehe :\n```\n{error_message}\n```",
            color=0xFF0000
        )
        await message.edit(embed=embed_error)

    except Exception as e:
        embed_error = discord.Embed(
            title="Erreur inconnue",
            description=f"Une erreur inattendue s'est produite : `{str(e)}`",
            color=0xFF0000
        )
        await message.edit(embed=embed_error)

ALLOWED_CHANNEL_ID = 1328058756969402501 # ID du canal autorisé

@bot.command()
async def sherlock(ctx, username: str):
    if str(ctx.channel.id) != str(1328058756969402501):
        await ctx.send(embed=discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être utilisée que dans un salon spécifique.",
            color=0xFF0000
        ))
        return

    sites = [
        f"https://github.com/{username}",
        f"https://www.linkedin.com/in/{username}",
        f"https://linktr.ee/{username}",
        f"https://www.snapchat.com/add/{username}",
        f"https://twitter.com/{username}",
        f"https://instagram.com/{username}",
        f"https://www.reddit.com/user/{username}",
        f"https://www.pinterest.com/{username}",
        f"https://www.twitch.tv/{username}",
        f"https://open.spotify.com/user/{username}",
        f"https://www.roblox.com/user.aspx?username={username}",
        f"https://t.me/{username}",
        f"https://www.youtube.com/@{username}",
        f"https://api.mojang.com/users/profiles/minecraft/{username}",
        f"https://www.codewars.com/users/{username}",
        f"https://forum.hackthebox.eu/profile/{username}",
        f"https://replit.com/@{username}",
        f"https://www.chess.com/member/{username}",
        f"https://www.behance.net/{username}",
        f"https://www.soundcloud.com/{username}",
    ]

    valid_users = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    for url in sites:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            if re.search(username, response.text, re.IGNORECASE):
                valid_users.append(url)
        except HTTPError as e:
            if e.response.status_code in [404, 406]:
                continue
            else:
                print(f"HTTPError pour {url}: {e}")
        except SSLError as e:
            print(f"SSLError pour {url}: {e}")
        except RequestException as e:
            print(f"RequestException pour {url}: {e}")

    if valid_users:
        results = "\n".join(valid_users)
        embed_dm = discord.Embed(
            title="__Résultats :__",
            description=results,
            color=0xFF0000
        )
        embed_dm.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=67599d3b&is=67584bbb&hm=ae1cd2bef295ed58caa8bc0f52028ed394fa8a4f5be63ea7b52dedf016b2db63&")

        try:
            await ctx.author.send(embed=embed_dm)

            embed_done = discord.Embed(
                title="Résultat trouvé 🔎, vérifiez vos DMs !",
                description="⚠️ Vérifiez d'avoir activé vos messages privés !",
                color=0xFF0000
            )
            embed_done.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=67599d3b&is=67584bbb&hm=ae1cd2bef295ed58caa8bc0f52028ed394fa8a4f5be63ea7b52dedf016b2db63&")
            await ctx.send(embed=embed_done)
        except discord.Forbidden:
            await ctx.send("Je ne peux pas vous envoyer de DM. Vérifiez vos paramètres de confidentialité.")
    else:
        embed_no_results = discord.Embed(
            title="__Aucun résultat trouvé__",
            description="Aucune correspondance pour cet utilisateur.",
            color=0xFF0000
        )
        embed_no_results.set_image(url="https://cdn.discordapp.com/attachments/1286742520021254352/1314232326817054821/wldb_banner.png?ex=67599d3b&is=67584bbb&hm=ae1cd2bef295ed58caa8bc0f52028ed394fa8a4f5be63ea7b52dedf016b2db63&")
        await ctx.send(embed=embed_no_results)

@bot.command(name="mc")
async def mc(ctx, username: str):
    ALLOWED_CHANNEL_ID = 1328058756969402501 # ID du canal autorisé

    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        error_embed = discord.Embed(
            title="Erreur",
            description="Cette commande ne peut être utilisée que dans le canal spécifié.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Recherche Minecraft")
        await ctx.send(embed=error_embed)
        return

    mojang_api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"

    try:
        response = requests.get(mojang_api_url)
        response.raise_for_status()
        data = response.json()

        uuid = data.get("id")
        username = data.get("name")

        session_server_url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        session_response = requests.get(session_server_url)
        session_response.raise_for_status()
        textures_data = session_response.json()

        skin_url = None
        cape_url = None

        for property in textures_data.get("properties", []):
            if property.get("name") == "textures":
                decoded_textures = base64.b64decode(property.get("value")).decode('utf-8')
                textures = json.loads(decoded_textures)
                skin_url = textures.get("textures", {}).get("SKIN", {}).get("url", "Aucune")
                cape_url = textures.get("textures", {}).get("CAPE", {}).get("url", "Aucune")

        embed = discord.Embed(
            title="🎮 Informations du joueur",
            color=0xFF0000
        )
        embed.add_field(name="Username", value=username, inline=False)
        embed.add_field(name="UUID", value=uuid, inline=False)
        embed.add_field(name="Skin URL", value=f"[Cliquez ici]({skin_url})" if skin_url else "Aucune", inline=False)
        embed.add_field(name="Cape URL", value=f"[Cliquez ici]({cape_url})" if cape_url else "Aucune", inline=False)
        if skin_url:
            embed.set_thumbnail(url=skin_url)
        embed.set_footer(text="Recherche Minecraft")

        await ctx.send(embed=embed)

    except requests.exceptions.HTTPError:
        await ctx.send(embed=discord.Embed(
            title="Erreur",
            description=f"Impossible de trouver un joueur avec le pseudo `{username}`.",
            color=0xFF0000
        ))
    except Exception as e:
        await ctx.send(embed=discord.Embed(
            title="Erreur inconnue",
            description=f"Une erreur est survenue : {str(e)}",
            color=0xFF0000
        ))

@bot.command()
async def userinfo(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
    except discord.NotFound:
        await ctx.send("Utilisateur introuvable.")
        return

    created_at = user.created_at.strftime("%d/%m/%Y %H:%M:%S")
    is_bot = "Oui" if user.bot else "Non"
    discriminator = user.discriminator
    status = "Inconnu"
    member = ctx.guild.get_member(user.id) if ctx.guild else None
    is_nitro = "Non"
    badges = ["Aucun badge"]

    if member:
        is_nitro = "Oui" if member.premium_since else "Non"
        badges = [badge.name for badge in member.public_flags.all()] if member.public_flags else ["Aucun badge"]

    avatar_url = user.avatar.url if user.avatar else "https://www.example.com/default-avatar.png"

    embed = discord.Embed(title=f"Infos de {user.name}#{discriminator}", color=0xFF0000)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="Nom d'utilisateur", value=user.name, inline=False)
    embed.add_field(name="Mention", value=user.mention, inline=False)
    embed.add_field(name="Créé le", value=created_at, inline=False)
    embed.add_field(name="Bot ?", value=is_bot, inline=False)
    embed.add_field(name="Badges", value=", ".join(badges), inline=False)
    embed.set_thumbnail(url=avatar_url)
    embed.set_footer(text=".gg/kkuU6CbQBG")

    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx, ip: str):
    """Ping une IP ou un domaine."""
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "4", ip]
    else:
        cmd = ["ping", "-c", "4", ip]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            embed = discord.Embed(
                title="Résultat du ping",
                description=f"```\n{result.stdout}\n```",
                color=0x00FF00
            )
        else:
            embed = discord.Embed(
                title="Erreur lors du ping",
                description=f"```\n{result.stderr}\n```",
                color=0xFF0000
            )

        await ctx.author.send(embed=embed)
        confirmation_embed = discord.Embed(
            title="Résultat trouvé 🔎, vérifiez vos DMs !",
            description="⚠️ Vérifiez d'avoir activé vos messages privés !",
            color=0xFF0000
        )
        confirmation_embed.set_image(url="https://cdn.discordapp.com/attachments/1313886334296789083/1315327224739532851/wldb_banner.png?ex=6757016f&is=6755afef&hm=cb788c4472a80bf9a8e986142db549584d0e5b6e1dcd56be61750be3e95b9eab&")
        confirmation_embed.set_footer(text="#Projet")
        await ctx.send(embed=confirmation_embed)

    except Exception as e:
        error_embed = discord.Embed(
            title="Erreur",
            description=f"Une erreur s'est produite : {e}",
            color=0xFF0000
        )
        await ctx.send(embed=error_embed)

api_key = "Z3YxNFFKTUI3Uk1zVWpUTEFORW06NjRjWHNfbS1UeHV6cFJ2N0VlSHJkZ=="
client = SeekApiClient(api_key)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot_logs.log"), logging.StreamHandler()]
)

AUTHORIZED_CHANNEL_ID = 1328058756969402501 # ID du canal autorisé

@bot.command(name="seekbase")
async def seekbase(ctx, *, search_string: str):
    if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
        embed_error = discord.Embed(
            title="Commande non autorisée",
            description="Cette commande ne peut être utilisée que dans le canal autorisé.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)
        logging.warning(f"Tentative d'utilisation de la commande 'search' dans un canal non autorisé par {ctx.author} (ID: {ctx.author.id}).")
        return

    logging.info(f"Commande 'search' exécutée par {ctx.author} (ID: {ctx.author.id}). Terme recherché : '{search_string}'")

    embed_loading = discord.Embed(
        title="Recherche en cours",
        description=f"Veuillez patienter pendant que je recherche des résultats pour : `{search_string}`.",
        color=discord.Color.blurple()
    )
    message = await ctx.send(embed=embed_loading)

    try:
        documents = client.search_documents(search_string, display_filename=True, size=1000)

        if not documents:
            embed_no_results = discord.Embed(
                title="Aucun résultat",
                description=f"Aucun document trouvé pour la recherche : `{search_string}`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed_no_results)
            logging.info(f"Aucun résultat trouvé pour '{search_string}'.")
        else:
            response = f"Résultats pour '{search_string}' :\n\n"
            for doc in documents[:500]:
                filename = doc.get("filename", "Inconnu")
                content = doc.get("content", "Aucun contenu disponible")

                response += f"\n»»————- ★ Found in : {filename} ★ ————-««\n\n"
                response += f"{content}\n"

            if len(response) > 2000:
                with open("search_results.txt", "w", encoding="utf-8") as f:
                    f.write(response)
                await ctx.author.send("Les résultats de votre recherche sont trop longs pour être affichés ici. Voici un fichier contenant les détails :", file=discord.File("search_results.txt"))
                logging.info(f"Résultats envoyés à {ctx.author} (ID: {ctx.author.id}) via fichier.")
            else:
                await ctx.author.send(response)
                logging.info(f"Résultats envoyés à {ctx.author} (ID: {ctx.author.id}) dans un message direct.")

            embed_success = discord.Embed(
                title="Résultats envoyés",
                description=f"Les résultats de votre recherche ont été envoyés en message privé.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed_success)

    except Exception as e:
        logging.error(f"Erreur lors de la recherche pour '{search_string}': {e}")
        embed_error = discord.Embed(
            title="Erreur",
            description=f"Une erreur est survenue lors de la recherche : `{e}`.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)



async def seekbase(ctx, *, search_string: str):
    if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
        embed_error = discord.Embed(
            title="Commande non autorisée",
            description="Cette commande ne peut être utilisée que dans le canal autorisé.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)
        logging.warning(f"Tentative d'utilisation de la commande 'search' dans un canal non autorisé par {ctx.author} (ID: {ctx.author.id}).")
        return




@bot.command(name="stop")
async def stop(ctx):
    """Arrête le bot uniquement dans le salon autorisé."""
    if ctx.channel.id != 1328058756969402501:  # ID du canal autorisé
        embed_error = discord.Embed(
            title="Commande non autorisée",
            description="Cette commande ne peut être utilisée que dans le canal autorisé.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)
        return

    await ctx.send("Arrêt du bot en cours...")
    await asyncio.sleep(1)
    await ctx.send("Bot arrêté.")
    await bot.close()
    

@bot.command(name="restart")
async def reboot(ctx):
    """Redémarre le bot uniquement dans le salon autorisé."""
    if ctx.channel.id != 1328058756969402501:  # ID du canal autorisé
        embed_error = discord.Embed(
            title="Commande non autorisée",
            description="Cette commande ne peut être utilisée que dans le canal autorisé.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)
        return

    await ctx.send("Redémarrage du bot en cours...")
    await asyncio.sleep(1.5)
    await ctx.send("Redémarrage terminer.")
    os.execl(sys.executable, sys.executable, *sys.argv)

bot.run(TOKEN)
