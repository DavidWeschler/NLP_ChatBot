import requests
from bs4 import BeautifulSoup

# Function to extract street names from a given city or area page
def extract_streets_from_city(city_url):
    # Send a GET request to the city/area URL
    response = requests.get(city_url)
    
    # Check if the response was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <a> tags that contain street names
        street_links = soup.find_all('a', href=True)
        
        streets = []
        
        # Loop through the links and extract the street names
        for link in street_links:
            street_name = link.get('alt')
            if street_name:  # We check if the 'alt' attribute exists
                streets.append(street_name)
        
        return streets
    else:
        print(f"Failed to retrieve the page: {city_url}")
        return []

# Example: scraping a specific URL
city_urls = [
    'https://geographic.org/streetview/israel/tel_aviv/ramat_gan/ramat_gan/bnei_brak.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/elad.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/ganei_tikva.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/gat_rimmon.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/givat_shmuel.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/kafr_bara.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/kafr_kasim.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/kfar_sirkin.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/magshimim.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/mazor.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/nehalim.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/nofech.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/petah_tikva.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/rinnatya.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/rosh_haayin.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/savyon.html',
    'https://geographic.org/streetview/israel/central/petah_tikva/petah_tiqwa/yehud.html',
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/givat_hen.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/hagor.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/hod_hasharon.html",

    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/jaljulya.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/kfar_malal.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/kfar_sava.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/kokhav_yair.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/matan.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/neve_yamin.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/nirit.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/raanana.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/ramot_hashavim.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/sde_warburg.html",
    "https://geographic.org/streetview/israel/central/petah_tikva/southern_sharon/zur_izhak.html",
    'https://geographic.org/streetview/israel/central/ramla/lod/gimzo.html',
    'https://geographic.org/streetview/israel/central/ramla/lod/lapid.html',
    'https://geographic.org/streetview/israel/central/ramla/lod/modiin_maccabim_reut.html',
    'https://geographic.org/streetview/israel/central/ramla/lod/nof_ayalon.html',
    'https://geographic.org/streetview/israel/central/ramla/lod/shilat.html',
    # "https://geographic.org/streetview/israel/central/ramla/ramla/ירושלים.html",    # !!
    "https://geographic.org/streetview/israel/central/ramla/ramla/ahisamakh.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/bait_dagan.html",
    # "https://geographic.org/streetview/israel/central/ramla/ramla/be'er_ya'akov.html",  # !!
    "https://geographic.org/streetview/israel/central/ramla/ramla/beit_nehemya.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/ben_shemen.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/bet_hashmonay.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/ginnaton.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/hadid.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/hemed.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/karmei_yosef.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/kefar_habad.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/kefar_shemuel.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/kefar_truman.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/kfar_bin_nun.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/lod.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/mazliah.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/mishmar_hashiva.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/nir_tzvi.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/ramla.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/ramot_meir.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/shoham.html",
    "https://geographic.org/streetview/israel/central/ramla/ramla/zafriyya.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/aseret.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/bnei_ayish.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/gan_yavne.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/ganei_yohanan.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/gedera.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/kfar_bilu.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/kfar_mordechai.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/kidron.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/kiryat_ekron.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/mazkeret_batya.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/nir_gallim.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/rehovot.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/yad_binyamin.html",
    "https://geographic.org/streetview/israel/central/rehovot/rehovot/yavne.html",
    "https://geographic.org/streetview/israel/central/rehovot/rishon_leziyyon/ness_ziona.html",
    "https://geographic.org/streetview/israel/central/rehovot/rishon_leziyyon/rishon_lezion.html",
    "https://geographic.org/streetview/israel/central/sharon/eastren_sharon/ahituv.html",
    "https://geographic.org/streetview/israel/central/sharon/eastren_sharon/bahan.html",
    "https://geographic.org/streetview/israel/central/sharon/eastren_sharon/bat_hefer.html",
    "https://geographic.org/streetview/israel/central/sharon/eastren_sharon/be'erotaim.html",   #!!
    "https://geographic.org/streetview/israel/central/sharon/eastren_sharon/kalanswa.html",
    "https://geographic.org/streetview/israel/central/sharon/eastren_sharon/taibe.html",
    "https://geographic.org/streetview/israel/central/sharon/eastren_sharon/tira.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/avihayil.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/beit_yanai.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/beit_yehoshua.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/beit_yitzhak_shaar_hefer.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/bney_dror.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/burgata.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/ein_vered.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/elyachin.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/even_yehuda.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/gannot_hadar.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/geullim.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/hadar_am.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/haniel.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/havazelet_hasharon.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/hofit.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/kadima.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/kefar_vitkin.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/kfar_haroeh.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/kfar_netter.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/kfar_yedidya.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/kfar_yona.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/michmoret.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/netanya.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/nordiyya.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/pardesiyya.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/tel_mond.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/tenuvot.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/udim.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/yanuv.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/zukey_yam.html",
    "https://geographic.org/streetview/israel/central/sharon/western_sharon/zur_moshe.html",
    'https://geographic.org/streetview/israel/haifa/hadera/alexander_mountain/harish.html',
    "https://geographic.org/streetview/israel/haifa/hadera/alexander_mountain/umm_el_fahm.html",
    "https://geographic.org/streetview/israel/haifa/hadera/hadera/baqa_al_gharbiyye.html",
    "https://geographic.org/streetview/israel/haifa/hadera/hadera/binyamina_givat_ada.html",
    "https://geographic.org/streetview/israel/haifa/hadera/hadera/caesarea.html",
    "https://geographic.org/streetview/israel/haifa/hadera/hadera/hadera.html",
    "https://geographic.org/streetview/israel/haifa/hadera/hadera/or_akiva.html",
    "https://geographic.org/streetview/israel/haifa/hadera/hadera/pardes_hanna_karkur.html",
    "https://geographic.org/streetview/israel/haifa/hadera/karmel_coast/atlit.html",
    "https://geographic.org/streetview/israel/haifa/hadera/zikhron_yaaqov/zikhron_yaakov.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/daliat_el_karmel.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/haifa.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/kfar_hasidim_bet.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/kiryat_ata.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/kiryat_bialik.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/kiryat_hayim.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/kiryat_motzkin.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/kiryat_tivon.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/kiryat_yam.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/nesher.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/nofit.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/rekhasim.html",
    "https://geographic.org/streetview/israel/haifa/haifa/haifa/tirat_carmel.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_footthills/judean_footthills/bet_shemesh.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/abu_ghaush.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/bar_giyyora.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/bet_zayit.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/even_sappir.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/givat_yearim.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/jerusalem.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/kiryat_ye_arim.html", # !!
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/mevaseret_zion.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/mevo_beitar.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/motza_illit.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/nes_harim.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/neve_ilan.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/ora.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/shoresh.html",
    "https://geographic.org/streetview/israel/jerusalem/judean_mountains/judean_mountains/zur_hadassa.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/alfei_menashe/alfei_menashe/alfei_menashe.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/alon_shvut/alon_shvut/alon_shvut.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/ariel/ariel/ariel.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/barqan/barqan/barqan.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/beit_arye/beit_arye/beit_arye.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/beit_el/beit_el/beit_el.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/beitar_illit/beitar_illit/beitar_illit.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/efrat/efrat/efrat.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/elazar/elazar/elazar.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/eli/eli/eli.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/elkana/elkana/elkana.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/emanuel/emanuel/emanuel.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/ets_efraim/ets_efraim/ets_efraim.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/givat_zeev/givat_zeev/givat_zeev.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/givon_hahadasha/givon_hahadasha/givon_hahadasha.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/halamish/halamish/halamish.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/har_adar/har_adar/har_adar.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/har_gilo/har_gilo/har_gilo.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/hashmonaim/hashmonaim/hashmonaim.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/karmei_tzur/karmei_tzur/karmei_tzur.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/karnei_shomron/karnei_shomron/karnei_shomron.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/kdumim/kdumim/kdumim.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/kfar_haoranin/kfar_haoranin/kfar_haoranin.html",    # !!
    "https://geographic.org/streetview/israel/judea_and_samaria/kiryat_arba/kiryat_arba/kiryat_arba.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/maale_adumim/maale_adumim/maale_adumim.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/maale_efraim/maale_efraim/maale_efraim.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/maale_shomron/maale_shomron/maale_shomron.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/matityahu/matityahu/matityahu.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/modiin_illit/modiin_illit/modiin_illit.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/neve_daniel/neve_daniel/neve_daniel.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/ofra/ofra/ofra.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/oranit/oranit/oranit.html",
    "https://geographic.org/streetview/israel/judea_and_samaria/shaarei_tikva/shaarei_tikva/shaarei_tikva.html",
    "https://geographic.org/streetview/israel/northern/akko/akko/acre.html",
    "https://geographic.org/streetview/israel/northern/akko/karmiel/karmiel.html",
    "https://geographic.org/streetview/israel/northern/akko/karmiel/rama.html",
    "https://geographic.org/streetview/israel/northern/akko/nahariyya/kafr_yasif.html",
    "https://geographic.org/streetview/israel/northern/akko/nahariyya/nahariya.html",
    "https://geographic.org/streetview/israel/northern/akko/nahariyya/regba.html",
    "https://geographic.org/streetview/israel/northern/akko/nahariyya/shave_ziyyon.html",
    "https://geographic.org/streetview/israel/northern/akko/nahariyya/shlomi.html",
    "https://geographic.org/streetview/israel/northern/akko/shefaram/adi.html",
    "https://geographic.org/streetview/israel/northern/akko/shefaram/arrabe.html",
    "https://geographic.org/streetview/israel/northern/akko/shefaram/moreshet.html",
    "https://geographic.org/streetview/israel/northern/akko/shefaram/sakhnin.html",
    "https://geographic.org/streetview/israel/northern/akko/shefaram/shefaram.html",
    "https://geographic.org/streetview/israel/northern/akko/shefaram/tamra.html",
    "https://geographic.org/streetview/israel/northern/akko/yehiam/kfar_vradim.html",
    "https://geographic.org/streetview/israel/northern/akko/yehiam/maalot_tarshiha.html",
    "https://geographic.org/streetview/israel/northern/akko/yehiam/meona.html",
    "https://geographic.org/streetview/israel/northern/golan/middle_golan/katzrin.html",
    "https://geographic.org/streetview/israel/northern/golan/southern_golan/bnei_yehuda.html",
    "https://geographic.org/streetview/israel/northern/kinneret/eastren_lower_galilee/givat_avni.html",
    "https://geographic.org/streetview/israel/northern/kinneret/eastren_lower_galilee/kfar_tavor.html",
    "https://geographic.org/streetview/israel/northern/kinneret/eastren_lower_galilee/yavneel.html",
    "https://geographic.org/streetview/israel/northern/kinneret/kinerot/kinneret_moshava.html",
    "https://geographic.org/streetview/israel/northern/kinneret/kinerot/menahemya.html",
    "https://geographic.org/streetview/israel/northern/kinneret/kinerot/migdal.html",
    "https://geographic.org/streetview/israel/northern/kinneret/kinerot/tiberias.html",
    "https://geographic.org/streetview/israel/northern/yizreel/bet_shean_basin/beit_shean.html",
    "https://geographic.org/streetview/israel/northern/yizreel/harod_valley/beit_alfa.html",
    "https://geographic.org/streetview/israel/northern/yizreel/harod_valley/gan_ner.html",
    "https://geographic.org/streetview/israel/northern/yizreel/kokhav_plateau/gazit.html",
    "https://geographic.org/streetview/israel/northern/yizreel/ma_gilboa/ma_gilboa.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/bueina.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/givat_ela.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/kaabiyye_tabbash_hajajre.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/kafr_kanna.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/migdal_haemek.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/nazareth.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/nazareth_illit.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/shimshit.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/timrat.html",
    "https://geographic.org/streetview/israel/northern/yizreel/nazareth_tiran_mountains/yafa_an_naseriyye.html",
    "https://geographic.org/streetview/israel/northern/yizreel/yizreel_basin/afula.html",
    "https://geographic.org/streetview/israel/northern/yizreel/yizreel_basin/ahuzat_barak.html",
    "https://geographic.org/streetview/israel/northern/yizreel/yizreel_basin/nahalal.html",
    "https://geographic.org/streetview/israel/northern/yizreel/yoqneam/alonim.html",
    "https://geographic.org/streetview/israel/northern/yizreel/yoqneam/ramat_yishai.html",
    "https://geographic.org/streetview/israel/northern/yizreel/yoqneam/ramat_yishai.html",
    "https://geographic.org/streetview/israel/northern/yizreel/yoqneam/yokneam_illit.html",
    "https://geographic.org/streetview/israel/northern/zefat/eastren_upper_galilee/safed.html",
    "https://geographic.org/streetview/israel/northern/zefat/hazor/hatzor_haglilit.html",
    "https://geographic.org/streetview/israel/northern/zefat/hazor/rosh_pina.html",
    "https://geographic.org/streetview/israel/northern/zefat/hula_basin/metula.html",
    "https://geographic.org/streetview/israel/northern/zefat/hula_basin/qiryat_shemona.html",
    "https://geographic.org/streetview/israel/northern/zefat/hula_basin/shear_yashuv.html",
    "https://geographic.org/streetview/israel/northern/zefat/hula_basin/snir.html",
    "https://geographic.org/streetview/israel/northern/zefat/hula_basin/yesud_hamaala.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/ashdod/ashdod.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/ashqelon/ashkelon.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/ashqelon/nitzan_bet.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/ashqelon/nizzan.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/ashqelon/sderot.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/lakhish/bney_dekalim.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/lakhish/kiryat_gat.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/lakhish/nehora.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/lakhish/yad_natan.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/ahva.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/arugot.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/kfar_harif.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/kiryat_malakhi.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/menuha.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/merkaz_shapira.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/sgula.html",
    "https://geographic.org/streetview/israel/southern/ashkelon/malakhi/shetulim.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/arava/eilat.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/arava/sappir.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/beer_sheva/arad.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/beer_sheva/beersheva.html",   # !!
    "https://geographic.org/streetview/israel/southern/beer_sheva/beer_sheva/lehavim.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/beer_sheva/meitar.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/beer_sheva/omer.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/beer_sheva/rahat.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/beer_sheva/tel_sheva.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/besor/ein_habsor.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/besor/ofakim.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/besor/prigan.html",   # !!
    "https://geographic.org/streetview/israel/southern/beer_sheva/besor/yated.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/gerar/mabbuim.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/gerar/netivot.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/northern_negev_mountain/dimona.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/northern_negev_mountain/mitspe_ramon.html",
    "https://geographic.org/streetview/israel/southern/beer_sheva/northern_negev_mountain/yeruham.html",
    "https://geographic.org/streetview/israel/tel_aviv/ben_gurion_airport/ben_gurion_airport/ben_gurion_airport.html",
    "https://geographic.org/streetview/israel/tel_aviv/holon/holon/azor.html",
    "https://geographic.org/streetview/israel/tel_aviv/holon/holon/bat_yam.html",
    "https://geographic.org/streetview/israel/tel_aviv/holon/holon/holon.html",
    "https://geographic.org/streetview/israel/tel_aviv/kiryat_airport/kiryat_airport/kiryat_airport.html",  
    "https://geographic.org/streetview/israel/tel_aviv/ramat_gan/ramat_gan/bnei_brak.html",
    "https://geographic.org/streetview/israel/tel_aviv/ramat_gan/ramat_gan/giv_atayim.html",    # !!
    "https://geographic.org/streetview/israel/tel_aviv/ramat_gan/ramat_gan/kiryat_ono.html",
    "https://geographic.org/streetview/israel/tel_aviv/ramat_gan/ramat_gan/or_yehuda.html",
    "https://geographic.org/streetview/israel/tel_aviv/ramat_gan/ramat_gan/ramat_gan.html",
    "https://geographic.org/streetview/israel/tel_aviv/tel_aviv/tel_aviv/herzliya.html",
    "https://geographic.org/streetview/israel/tel_aviv/tel_aviv/tel_aviv/kefar_shemaryahu.html",
    "https://geographic.org/streetview/israel/tel_aviv/tel_aviv/tel_aviv/ramat_hasharon.html",
    "https://geographic.org/streetview/israel/tel_aviv/tel_aviv/tel_aviv/tel_aviv_jaffa.html"

    ]


def main():
    streets = []
    
    with open("streets_200-288.txt", "w", encoding="utf-8") as file:

        for i in range(200, 288):
            streets_in = extract_streets_from_city(city_urls[i])
            streets += list(set(streets_in))

            for street in streets:
                file.write(f"{street}\n")
            
            if i == 287:
                print(f"last url: {city_urls[i]}")


# print("Start!")
# main()
# print("Done!")

x = 21233 + 16190 + 134501 + 585791 + 322781
print(x)




