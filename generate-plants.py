#!/usr/bin/env python3
"""Generate plants.js with 30 levels per category using Wikipedia API for images."""

import json
import urllib.request
import urllib.parse
import time
import sys

# 30 levels × 5 plants = 150 plants per category
CATEGORIES = {
    "indoor": {
        "name": "Krukväxter",
        "icon": "🪴",
        "description": "Lär dig vanliga inomhusväxter",
        "color": "from-green-400 to-green-600",
        "levels": [
            {"name": "Nybörjare 1", "plants": [
                ("Monstera", "Monstera_deliciosa"), ("Fredskalla", "Spathiphyllum"), ("Gullranka", "Epipremnum_aureum"),
                ("Svärmorstunga", "Sansevieria_trifasciata"), ("Aloe vera", "Aloe_vera")]},
            {"name": "Nybörjare 2", "plants": [
                ("Fikus", "Ficus_benjamina"), ("Pelargon", "Pelargonium"), ("Orkidé", "Phalaenopsis"),
                ("Bégonia", "Begonia"), ("Elefantöra", "Alocasia")]},
            {"name": "Nybörjare 3", "plants": [
                ("Strelitzia", "Strelitzia"), ("Calathea", "Calathea"), ("Pilea", "Pilea_peperomioides"),
                ("Kentiapalm", "Howea_forsteriana"), ("Philodendron", "Philodendron")]},
            {"name": "Populära 1", "plants": [
                ("Julstjärna", "Euphorbia_pulcherrima"), ("Gerbera", "Gerbera"), ("Krysantemum", "Chrysanthemum"),
                ("Azalea", "Azalea"), ("Cyklamen", "Cyclamen")]},
            {"name": "Populära 2", "plants": [
                ("Tradescantia", "Tradescantia"), ("Dracena", "Dracaena_(plant)"), ("Syngonium", "Syngonium"),
                ("Maranta", "Maranta"), ("Zamioculcas", "Zamioculcas")]},
            {"name": "Populära 3", "plants": [
                ("Bonsai", "Bonsai"), ("Klätterfikonträd", "Ficus_pumila"), ("Kroton", "Codiaeum_variegatum"),
                ("Skärmpalm", "Chamaedorea_elegans"), ("Fredlilja", "Anthurium")]},
            {"name": "Kaktusar 1", "plants": [
                ("Opuntia", "Opuntia"), ("Mammillaria", "Mammillaria"), ("Echinokaktus", "Echinocactus"),
                ("Cereus", "Cereus_(plant)"), ("Rhipsalis", "Rhipsalis")]},
            {"name": "Kaktusar 2", "plants": [
                ("Julkaktus", "Schlumbergera"), ("Påskkaktus", "Hatiora"), ("Gymnocalycium", "Gymnocalycium"),
                ("Rebutia", "Rebutia"), ("Ferocactus", "Ferocactus")]},
            {"name": "Suckulenter 1", "plants": [
                ("Echeveria", "Echeveria"), ("Crassula", "Crassula"), ("Haworthia", "Haworthia"),
                ("Sedum", "Sedum"), ("Sempervivum", "Sempervivum")]},
            {"name": "Suckulenter 2", "plants": [
                ("Lithops", "Lithops"), ("Euphorbia", "Euphorbia"), ("Senecio", "Curio_rowleyanus"),
                ("Kalanchoe", "Kalanchoe"), ("Aeonium", "Aeonium")]},
            {"name": "Ormbunkar", "plants": [
                ("Bräken", "Nephrolepis_exaltata"), ("Hjorttunga", "Asplenium_nidus"),
                ("Silverbräken", "Pteris"), ("Adiantum", "Adiantum"), ("Trädormbunke", "Cyathea")]},
            {"name": "Palmer", "plants": [
                ("Areca", "Dypsis_lutescens"), ("Kokospalm", "Cocos_nucifera"), ("Dvärgpalm", "Chamaerops"),
                ("Fishtail palm", "Caryota"), ("Sagopalm", "Cycas_revoluta")]},
            {"name": "Klätterväxter 1", "plants": [
                ("Murgröna", "Hedera_helix"), ("Passionsblomma", "Passiflora"), ("Hoya", "Hoya"),
                ("Jasmin", "Jasminum"), ("Cissus", "Cissus")]},
            {"name": "Klätterväxter 2", "plants": [
                ("Vaniljblomma", "Vanilla_(genus)"), ("Klockranka", "Cobaea_scandens"),
                ("Dipladenia", "Mandevilla"), ("Klätterväxt", "Stephanotis_floribunda"),
                ("Columnea", "Columnea")]},
            {"name": "Lövväxter 1", "plants": [
                ("Dieffenbachia", "Dieffenbachia"), ("Schefflera", "Schefflera"), ("Pachira", "Pachira_aquatica"),
                ("Fittonia", "Fittonia"), ("Peperomia", "Peperomia")]},
            {"name": "Lövväxter 2", "plants": [
                ("Yucca", "Yucca"), ("Ctenanthe", "Ctenanthe"), ("Caladium", "Caladium"),
                ("Aglaonema", "Aglaonema"), ("Aspidistra", "Aspidistra")]},
            {"name": "Blommande 1", "plants": [
                ("Hibiskus", "Hibiscus"), ("Gardenia", "Gardenia"), ("Fuchsia", "Fuchsia"),
                ("Kamelja", "Camellia"), ("Plumeria", "Plumeria")]},
            {"name": "Blommande 2", "plants": [
                ("Citrus", "Citrus"), ("Gloxinia", "Sinningia_speciosa"), ("Saintpaulia", "Streptocarpus_sect._Saintpaulia"),
                ("Vriesea", "Vriesea"), ("Guzmania", "Guzmania")]},
            {"name": "Blommande 3", "plants": [
                ("Kliva", "Clivia"), ("Amaryllis", "Amaryllis"), ("Oleander", "Nerium"),
                ("Bouganvillea", "Bougainvillea"), ("Kalanchoë", "Kalanchoe_blossfeldiana")]},
            {"name": "Luftrenare", "plants": [
                ("Guldpalm", "Chrysalidocarpus_lutescens"), ("Fredlilja", "Chlorophytum_comosum"),
                ("Druvjärnek", "Dracaena_fragrans"), ("Bambupalm", "Chamaedorea_seifrizii"),
                ("Gummiträd", "Ficus_elastica")]},
            {"name": "Ovanliga 1", "plants": [
                ("Venusflugfälla", "Dionaea_muscipula"), ("Silkesträd", "Mimosa_pudica"),
                ("Luftväxt", "Tillandsia"), ("Nepenthes", "Nepenthes"), ("Sarracenia", "Sarracenia")]},
            {"name": "Ovanliga 2", "plants": [
                ("Kokosoljeplanta", "Jatropha_podagrica"), ("Elefantfot", "Beaucarnea_recurvata"),
                ("Pengaträd", "Crassula_ovata"), ("Paraplypalm", "Cyperus_alternifolius"),
                ("Avokado", "Persea_americana")]},
            {"name": "Tropiska 1", "plants": [
                ("Bananpalm", "Musa_(genus)"), ("Ingefära", "Zingiber"), ("Bromeliaceae", "Bromeliaceae"),
                ("Heliconia", "Heliconia"), ("Ananas", "Pineapple")]},
            {"name": "Tropiska 2", "plants": [
                ("Medinilla", "Medinilla"), ("Rafflesia", "Rafflesia"), ("Frangipani", "Plumeria"),
                ("Ixora", "Ixora"), ("Anthurium", "Anthurium")]},
            {"name": "Sällsynta 1", "plants": [
                ("Monstera Thai", "Monstera_deliciosa"), ("Variegata", "Variegation"),
                ("Hoya kerrii", "Hoya_kerrii"), ("Begonia maculata", "Begonia_maculata"),
                ("Alocasia zebrina", "Alocasia_zebrina")]},
            {"name": "Sällsynta 2", "plants": [
                ("Dischidia", "Dischidia"), ("Ceropegia", "Ceropegia"), ("Pseudolithos", "Pseudolithos"),
                ("Welwitschia", "Welwitschia"), ("Titanopsis", "Titanopsis")]},
            {"name": "Japanska", "plants": [
                ("Bonsai fikus", "Ficus_retusa"), ("Japansk lönn", "Acer_palmatum"),
                ("Azalea bonsai", "Rhododendron"), ("Bambu", "Bamboo"), ("Wisteria", "Wisteria")]},
            {"name": "Medelhavet", "plants": [
                ("Olivträd", "Olive"), ("Laurbär", "Laurus_nobilis"), ("Citronträd", "Citrus_limon"),
                ("Apelsinträd", "Citrus_sinensis"), ("Fikonträd", "Ficus_carica")]},
            {"name": "Expert 1", "plants": [
                ("Stapelia", "Stapelia"), ("Adenium", "Adenium"), ("Pachypodium", "Pachypodium"),
                ("Euphorbia trigona", "Euphorbia_trigona"), ("Testudinaria", "Dioscorea_elephantipes")]},
            {"name": "Expert 2", "plants": [
                ("Dracula orkidé", "Dracula_(plant)"), ("Bulbophyllum", "Bulbophyllum"),
                ("Dendrobium", "Dendrobium"), ("Vanda", "Vanda"), ("Oncidium", "Oncidium")]},
        ],
    },
    "kitchen": {
        "name": "Köksväxter",
        "icon": "🥬",
        "description": "Grönsaker och kryddor",
        "color": "from-lime-400 to-lime-600",
        "levels": [
            {"name": "Grönsaker 1", "plants": [
                ("Tomat", "Tomato"), ("Gurka", "Cucumber"), ("Morot", "Carrot"),
                ("Lök", "Onion"), ("Potatis", "Potato")]},
            {"name": "Grönsaker 2", "plants": [
                ("Paprika", "Bell_pepper"), ("Sallat", "Lettuce"), ("Broccoli", "Broccoli"),
                ("Blomkål", "Cauliflower"), ("Spenat", "Spinach")]},
            {"name": "Grönsaker 3", "plants": [
                ("Aubergine", "Eggplant"), ("Purjolök", "Leek"), ("Selleri", "Celery"),
                ("Fänkål", "Fennel"), ("Kronärtskocka", "Globe_artichoke")]},
            {"name": "Kryddor 1", "plants": [
                ("Basilika", "Basil"), ("Dill", "Dill"), ("Persilja", "Parsley"),
                ("Rosmarin", "Rosemary"), ("Timjan", "Thyme")]},
            {"name": "Kryddor 2", "plants": [
                ("Oregano", "Oregano"), ("Mynta", "Mentha"), ("Koriander", "Coriander"),
                ("Salvia", "Salvia_officinalis"), ("Dragon", "Tarragon")]},
            {"name": "Kryddor 3", "plants": [
                ("Mejram", "Marjoram"), ("Citronmeliss", "Lemon_balm"), ("Lagerblad", "Bay_laurel"),
                ("Gräslök", "Chives"), ("Libbsticka", "Lovage")]},
            {"name": "Bär 1", "plants": [
                ("Jordgubbe", "Strawberry"), ("Hallon", "Raspberry"), ("Blåbär", "Blueberry"),
                ("Björnbär", "Blackberry"), ("Lingon", "Lingonberry")]},
            {"name": "Bär 2", "plants": [
                ("Krusbär", "Gooseberry"), ("Vinbär", "Redcurrant"), ("Svartvinbär", "Blackcurrant"),
                ("Hjortron", "Rubus_chamaemorus"), ("Tranbär", "Cranberry")]},
            {"name": "Bär 3", "plants": [
                ("Havtorn", "Hippophae"), ("Aronia", "Aronia"), ("Fläder", "Sambucus"),
                ("Nypon", "Rose_hip"), ("Slånbär", "Prunus_spinosa")]},
            {"name": "Rotfrukter 1", "plants": [
                ("Rödbetor", "Beetroot"), ("Palsternacka", "Parsnip"), ("Kålrot", "Rutabaga"),
                ("Rova", "Turnip"), ("Jordärtskocka", "Jerusalem_artichoke")]},
            {"name": "Rotfrukter 2", "plants": [
                ("Rädisa", "Radish"), ("Pepparrot", "Horseradish"), ("Sötpotatis", "Sweet_potato"),
                ("Ingefära", "Ginger"), ("Gurkmeja", "Turmeric")]},
            {"name": "Kål 1", "plants": [
                ("Vitkål", "Cabbage"), ("Rödkål", "Red_cabbage"), ("Grönkål", "Kale"),
                ("Brysselkål", "Brussels_sprout"), ("Savoykål", "Savoy_cabbage")]},
            {"name": "Kål 2", "plants": [
                ("Pak choi", "Bok_choy"), ("Romanesco", "Romanesco_broccoli"), ("Kohlrabi", "Kohlrabi"),
                ("Mangold", "Chard"), ("Endiv", "Endive")]},
            {"name": "Baljväxter", "plants": [
                ("Sockerärta", "Snow_pea"), ("Gröna bönor", "Green_bean"), ("Bondböna", "Vicia_faba"),
                ("Linser", "Lentil"), ("Kikärta", "Chickpea")]},
            {"name": "Squash", "plants": [
                ("Zucchini", "Zucchini"), ("Butternut", "Butternut_squash"), ("Pumpa", "Pumpkin"),
                ("Spaghettisquash", "Spaghetti_squash"), ("Patisson", "Pattypan_squash")]},
            {"name": "Lökväxter", "plants": [
                ("Vitlök", "Garlic"), ("Schalottenlök", "Shallot"), ("Ramslök", "Allium_ursinum"),
                ("Vårlök", "Scallion"), ("Rödlök", "Red_onion")]},
            {"name": "Fruktgrönsaker", "plants": [
                ("Avokado", "Avocado"), ("Chilipeppar", "Chili_pepper"), ("Okra", "Okra"),
                ("Tomatillo", "Tomatillo"), ("Jalapeño", "Jalapeño")]},
            {"name": "Sallader", "plants": [
                ("Ruccola", "Arugula"), ("Isbergssallat", "Iceberg_lettuce"), ("Romansallat", "Romaine_lettuce"),
                ("Frisée", "Frisée"), ("Mâche", "Valerianella_locusta")]},
            {"name": "Asiatiska", "plants": [
                ("Wasabi", "Wasabi"), ("Sojaböna", "Soybean"), ("Bambuskott", "Bamboo_shoot"),
                ("Daikon", "Daikon"), ("Edamame", "Edamame")]},
            {"name": "Medelhavs", "plants": [
                ("Rucola", "Arugula"), ("Kapris", "Caper"), ("Radicchio", "Radicchio"),
                ("Portulak", "Portulaca_oleracea"), ("Rova", "Brassica_rapa")]},
            {"name": "Svampar 1", "plants": [
                ("Champinjon", "Agaricus_bisporus"), ("Kantarell", "Chanterelle"), ("Karl-Johan", "Boletus_edulis"),
                ("Shiitake", "Shiitake"), ("Trattkantarell", "Craterellus_tubaeformis")]},
            {"name": "Svampar 2", "plants": [
                ("Östronskivling", "Pleurotus_ostreatus"), ("Murkling", "Morchella"), ("Tryffel", "Truffle"),
                ("Enoki", "Enokitake"), ("Portobello", "Agaricus_bisporus")]},
            {"name": "Groddar", "plants": [
                ("Alfalfa", "Alfalfa"), ("Solrosgrodd", "Sunflower"), ("Ärtskott", "Pea_shoot"),
                ("Rödklöver", "Trifolium_pratense"), ("Bockhornsklöver", "Fenugreek")]},
            {"name": "Frukt 1", "plants": [
                ("Äpple", "Apple"), ("Päron", "Pear"), ("Plommon", "Plum"),
                ("Körsbär", "Cherry"), ("Aprikos", "Apricot")]},
            {"name": "Frukt 2", "plants": [
                ("Persika", "Peach"), ("Nektarin", "Nectarine"), ("Fikon", "Common_fig"),
                ("Kiwi", "Kiwifruit"), ("Vindruva", "Grape")]},
            {"name": "Exotisk frukt", "plants": [
                ("Mango", "Mango"), ("Passionsfrukt", "Passionfruit"), ("Papaya", "Papaya"),
                ("Granatäpple", "Pomegranate"), ("Lychee", "Lychee")]},
            {"name": "Citrusfrukter", "plants": [
                ("Citron", "Lemon"), ("Lime", "Lime_(fruit)"), ("Apelsin", "Orange_(fruit)"),
                ("Grapefrukt", "Grapefruit"), ("Mandarin", "Mandarin_orange")]},
            {"name": "Nötter", "plants": [
                ("Valnöt", "Walnut"), ("Hasselnöt", "Hazelnut"), ("Mandel", "Almond"),
                ("Pistagenöt", "Pistachio"), ("Cashewnöt", "Cashew")]},
            {"name": "Spannmål", "plants": [
                ("Vete", "Wheat"), ("Råg", "Rye"), ("Havre", "Oat"),
                ("Korn", "Barley"), ("Majs", "Maize")]},
            {"name": "Exotiska grönsaker", "plants": [
                ("Lotusrot", "Nelumbo_nucifera"), ("Taro", "Taro"), ("Cassava", "Cassava"),
                ("Jicama", "Pachyrhizus_erosus"), ("Chayote", "Chayote")]},
        ],
    },
    "perennials": {
        "name": "Perenner",
        "icon": "🌸",
        "description": "Fleråriga trädgårdsväxter",
        "color": "from-pink-400 to-pink-600",
        "levels": [
            {"name": "Populära 1", "plants": [
                ("Lavendel", "Lavandula"), ("Pion", "Peony"), ("Funkia", "Hosta"),
                ("Daglilja", "Hemerocallis"), ("Riddarsporre", "Delphinium")]},
            {"name": "Populära 2", "plants": [
                ("Astilbe", "Astilbe"), ("Bergenia", "Bergenia"), ("Brunnäva", "Geranium_phaeum"),
                ("Hasselört", "Asarum_europaeum"), ("Lungört", "Pulmonaria_officinalis")]},
            {"name": "Populära 3", "plants": [
                ("Solhatt", "Echinacea"), ("Stäppsalvia", "Salvia_nemorosa"), ("Kärleksört", "Hylotelephium"),
                ("Prydnadsgräs", "Miscanthus_sinensis"), ("Näva", "Geranium")]},
            {"name": "Vårblommor 1", "plants": [
                ("Snödroppe", "Galanthus"), ("Krokus", "Crocus"), ("Påsklilja", "Narcissus_(plant)"),
                ("Tulpan", "Tulip"), ("Hyacint", "Hyacinth_(plant)")]},
            {"name": "Vårblommor 2", "plants": [
                ("Scilla", "Scilla"), ("Vintergäck", "Eranthis"), ("Blåstjärna", "Chionodoxa"),
                ("Vitsippa", "Anemone_nemorosa"), ("Blåsippa", "Hepatica_nobilis")]},
            {"name": "Vårblommor 3", "plants": [
                ("Primula", "Primula"), ("Liljekonvalj", "Lily_of_the_valley"), ("Förgätmigej", "Myosotis"),
                ("Lungört", "Pulmonaria"), ("Gullviva", "Primula_veris")]},
            {"name": "Sommarblommande 1", "plants": [
                ("Flox", "Phlox"), ("Rudbeckia", "Rudbeckia"), ("Veronica", "Veronica_(plant)"),
                ("Ligularia", "Ligularia"), ("Akleja", "Aquilegia")]},
            {"name": "Sommarblommande 2", "plants": [
                ("Trädgårdsriddarsporre", "Delphinium"), ("Lupin", "Lupinus"), ("Stockros", "Alcea"),
                ("Fingerborgsblomma", "Digitalis"), ("Klockblomma", "Campanula")]},
            {"name": "Sommarblommande 3", "plants": [
                ("Jättedaggkåpa", "Alchemilla_mollis"), ("Vallmo", "Papaver"), ("Iris", "Iris_(plant)"),
                ("Lilja", "Lilium"), ("Kungsängslilja", "Fritillaria_imperialis")]},
            {"name": "Höstblommande", "plants": [
                ("Höstanemon", "Anemone_hupehensis"), ("Höstaster", "Aster_(genus)"), ("Chrysantemum", "Chrysanthemum"),
                ("Höstgullris", "Solidago"), ("Röllika", "Achillea_millefolium")]},
            {"name": "Gräs 1", "plants": [
                ("Blåsvingel", "Festuca_glauca"), ("Japanskt blodgräs", "Imperata_cylindrica"),
                ("Lampborstgräs", "Pennisetum"), ("Jättegräs", "Cortaderia_selloana"),
                ("Tuvrör", "Calamagrostis")]},
            {"name": "Gräs 2", "plants": [
                ("Diamantgräs", "Calamagrostis_brachytricha"), ("Eldgräs", "Stipa"),
                ("Hakonegräs", "Hakonechloa"), ("Storstarr", "Carex"), ("Kaveldun", "Typha")]},
            {"name": "Marktäckare 1", "plants": [
                ("Murgröna", "Hedera_helix"), ("Vintergröna", "Vinca"), ("Krypoxalis", "Oxalis"),
                ("Fetblad", "Sedum_acre"), ("Krypljung", "Erica_carnea")]},
            {"name": "Marktäckare 2", "plants": [
                ("Waldsteinia", "Waldsteinia"), ("Pachysandra", "Pachysandra"), ("Lamium", "Lamium"),
                ("Ajuga", "Ajuga"), ("Saxifraga", "Saxifraga")]},
            {"name": "Skuggväxter 1", "plants": [
                ("Rodgersia", "Rodgersia"), ("Trollius", "Trollius"), ("Tiarella", "Tiarella"),
                ("Heuchera", "Heuchera"), ("Brunnera", "Brunnera")]},
            {"name": "Skuggväxter 2", "plants": [
                ("Doftrams", "Aruncus"), ("Vipprams", "Astilbe"), ("Strutbräken", "Matteuccia"),
                ("Smörblomma", "Ranunculus"), ("Fackelblomster", "Lythrum")]},
            {"name": "Torktåliga 1", "plants": [
                ("Stenkyndel", "Clinopodium"), ("Lammöra", "Stachys_byzantina"),
                ("Silverpäron", "Artemisia_schmidtiana"), ("Kantnepeta", "Nepeta"),
                ("Stäppvädd", "Knautia")]},
            {"name": "Torktåliga 2", "plants": [
                ("Timjan", "Thymus"), ("Fetblad", "Sedum"), ("Kungsmynta", "Origanum_vulgare"),
                ("Bolltistel", "Echinops"), ("Jätteverbena", "Verbena_bonariensis")]},
            {"name": "Vattenväxter", "plants": [
                ("Näckros", "Nymphaea"), ("Vass", "Phragmites"), ("Svärdslilja", "Iris_pseudacorus"),
                ("Kabbleka", "Caltha_palustris"), ("Fackelblomster", "Lythrum_salicaria")]},
            {"name": "Klättrande", "plants": [
                ("Klematis", "Clematis"), ("Kaprifol", "Lonicera"), ("Humle", "Humulus_lupulus"),
                ("Vildvin", "Parthenocissus"), ("Klätterhortensia", "Hydrangea_anomala")]},
            {"name": "Lökväxter 1", "plants": [
                ("Allium", "Allium"), ("Dahlia", "Dahlia"), ("Gladiolus", "Gladiolus"),
                ("Crocosmia", "Crocosmia"), ("Agapanthus", "Agapanthus")]},
            {"name": "Lökväxter 2", "plants": [
                ("Snöklocka", "Leucojum"), ("Krollilja", "Lilium_martagon"), ("Turkisk lilja", "Lilium_lancifolium"),
                ("Hundtandslilja", "Erythronium"), ("Kejsarkrona", "Fritillaria")]},
            {"name": "Doftande", "plants": [
                ("Lavendel", "Lavandula_angustifolia"), ("Pion", "Paeonia_lactiflora"),
                ("Trädgårdsiris", "Iris_germanica"), ("Viol", "Viola_odorata"),
                ("Nattljus", "Oenothera")]},
            {"name": "Fjärilsväxter", "plants": [
                ("Syrenbuddleja", "Buddleja"), ("Verbena", "Verbena"), ("Röllika", "Achillea"),
                ("Prästkrage", "Leucanthemum"), ("Rudbeckia", "Rudbeckia_fulgida")]},
            {"name": "Stenparti 1", "plants": [
                ("Stenbräcka", "Saxifraga"), ("Alpklocka", "Soldanella"), ("Edelweiss", "Leontopodium_nivale"),
                ("Bergsnejlika", "Dianthus_alpinus"), ("Gentiana", "Gentiana")]},
            {"name": "Stenparti 2", "plants": [
                ("Aubrietia", "Aubrieta"), ("Arabis", "Arabis"), ("Alyssum", "Alyssum"),
                ("Phlox subulata", "Phlox_subulata"), ("Iberis", "Iberis")]},
            {"name": "Vintergröna", "plants": [
                ("Bergenia", "Bergenia_cordifolia"), ("Julros", "Helleborus"), ("Heuchera", "Heuchera"),
                ("Liriope", "Liriope_(plant)"), ("Epimedium", "Epimedium")]},
            {"name": "Medicinalväxter", "plants": [
                ("Johannesört", "Hypericum_perforatum"), ("Malört", "Artemisia_absinthium"),
                ("Valeriana", "Valeriana_officinalis"), ("Echinacea", "Echinacea_purpurea"),
                ("Kamomilla", "Chamomile")]},
            {"name": "Prärieväxter", "plants": [
                ("Prärieljus", "Gaura_lindheimeri"), ("Präriesolhatt", "Ratibida"), ("Indiangräs", "Sorghastrum_nutans"),
                ("Liatris", "Liatris"), ("Baptisia", "Baptisia")]},
            {"name": "Exotiska perenner", "plants": [
                ("Gunnera", "Gunnera"), ("Agave", "Agave"), ("Kniphofia", "Kniphofia"),
                ("Acanthus", "Acanthus_(plant)"), ("Beschorneria", "Beschorneria")]},
        ],
    },
    "trees": {
        "name": "Träd",
        "icon": "🌳",
        "description": "Svenska träd att känna igen",
        "color": "from-emerald-500 to-emerald-700",
        "levels": [
            {"name": "Vanliga 1", "plants": [
                ("Björk", "Betula_pendula"), ("Gran", "Picea_abies"), ("Tall", "Scots_pine"),
                ("Ek", "Quercus_robur"), ("Lönn", "Acer_platanoides")]},
            {"name": "Vanliga 2", "plants": [
                ("Asp", "Populus_tremula"), ("Lind", "Tilia_cordata"), ("Alm", "Ulmus_glabra"),
                ("Ask", "Fraxinus_excelsior"), ("Bok", "Fagus_sylvatica")]},
            {"name": "Fruktträd 1", "plants": [
                ("Äppelträd", "Apple"), ("Päronträd", "Pear"), ("Plommonträd", "Plum"),
                ("Körsbärsträd", "Cherry_blossom"), ("Hassel", "Corylus_avellana")]},
            {"name": "Fruktträd 2", "plants": [
                ("Valnötsträd", "Juglans_regia"), ("Aprikosträd", "Prunus_armeniaca"),
                ("Persikoträd", "Prunus_persica"), ("Fikonträd", "Ficus_carica"),
                ("Mullbärsträd", "Morus_(plant)")]},
            {"name": "Barrträd 1", "plants": [
                ("Lärk", "Larix"), ("Douglas", "Pseudotsuga_menziesii"), ("Silvergran", "Abies_alba"),
                ("Cypress", "Cupressus"), ("Thuja", "Thuja")]},
            {"name": "Barrträd 2", "plants": [
                ("En", "Juniperus_communis"), ("Idegran", "Taxus_baccata"), ("Hemlock", "Tsuga"),
                ("Sekvoja", "Sequoia"), ("Ceder", "Cedrus")]},
            {"name": "Sälg & Pil", "plants": [
                ("Sälg", "Salix_caprea"), ("Tårpil", "Salix_babylonica"), ("Korgvide", "Salix_viminalis"),
                ("Vitpil", "Salix_alba"), ("Gråvide", "Salix_cinerea")]},
            {"name": "Popplar", "plants": [
                ("Poppel", "Populus"), ("Balsampoppel", "Populus_balsamifera"), ("Silverpoppel", "Populus_alba"),
                ("Svartpoppel", "Populus_nigra"), ("Kanadapoppel", "Populus_deltoides")]},
            {"name": "Ädellövträd 1", "plants": [
                ("Avenbok", "Carpinus_betulus"), ("Kastanj", "Castanea_sativa"),
                ("Hästkastanj", "Aesculus_hippocastanum"), ("Platån", "Platanus"),
                ("Tulpanträd", "Liriodendron")]},
            {"name": "Ädellövträd 2", "plants": [
                ("Rödek", "Quercus_rubra"), ("Bergek", "Quercus_petraea"), ("Avenbok", "Carpinus"),
                ("Naverlönn", "Acer_campestre"), ("Skogslönn", "Acer_pseudoplatanus")]},
            {"name": "Prydnadsträd 1", "plants": [
                ("Magnolia", "Magnolia"), ("Japanskt körsbär", "Prunus_serrulata"),
                ("Ginkgo", "Ginkgo_biloba"), ("Katsura", "Cercidiphyllum"), ("Koralldogwood", "Cornus_kousa")]},
            {"name": "Prydnadsträd 2", "plants": [
                ("Blodbok", "Fagus_sylvatica_purpurea"), ("Hängbjörk", "Betula_pendula"),
                ("Rödbladig lönn", "Acer_palmatum"), ("Japansk lönn", "Acer_palmatum"),
                ("Pagodträd", "Styphnolobium_japonicum")]},
            {"name": "Tropiska träd", "plants": [
                ("Palm", "Arecaceae"), ("Bananträd", "Musa_(genus)"), ("Baobab", "Adansonia"),
                ("Mahogny", "Mahogany"), ("Teak", "Teak")]},
            {"name": "Nordamerikanska", "plants": [
                ("Sockerlönn", "Acer_saccharum"), ("Redwood", "Sequoia_sempervirens"),
                ("Mammutträd", "Sequoiadendron_giganteum"), ("Tulpanpoppel", "Liriodendron_tulipifera"),
                ("Hickory", "Carya")]},
            {"name": "Asiatiska", "plants": [
                ("Bambu", "Bamboo"), ("Kryptomeria", "Cryptomeria"), ("Ginko", "Ginkgo"),
                ("Paulownia", "Paulownia"), ("Zelkova", "Zelkova")]},
            {"name": "Medelhavsträd", "plants": [
                ("Olivträd", "Olive"), ("Korkek", "Quercus_suber"), ("Pinjeträd", "Stone_pine"),
                ("Johannesbröd", "Ceratonia_siliqua"), ("Eucalyptus", "Eucalyptus")]},
            {"name": "Skogsträd 1", "plants": [
                ("Rönn", "Sorbus_aucuparia"), ("Hägg", "Prunus_padus"), ("Oxel", "Sorbus_intermedia"),
                ("Fågelbär", "Prunus_avium"), ("Skogsalm", "Ulmus_laevis")]},
            {"name": "Skogsträd 2", "plants": [
                ("Klibbal", "Alnus_glutinosa"), ("Gråal", "Alnus_incana"), ("Häckoxel", "Sorbus"),
                ("Skogslind", "Tilia_platyphyllos"), ("Tysklönn", "Acer_pseudoplatanus")]},
            {"name": "Parkträd 1", "plants": [
                ("Blåregn", "Wisteria"), ("Robinia", "Robinia_pseudoacacia"),
                ("Katalpa", "Catalpa"), ("Ambra", "Liquidambar"), ("Cercis", "Cercis")]},
            {"name": "Parkträd 2", "plants": [
                ("Sofora", "Styphnolobium"), ("Gleditsia", "Gleditsia"), ("Pterocarya", "Pterocarya"),
                ("Metasekvoja", "Metasequoia"), ("Taxodium", "Taxodium")]},
            {"name": "Städsegröna", "plants": [
                ("Järnek", "Ilex"), ("Buxbom", "Buxus"), ("Lager", "Laurus"),
                ("Rhododendron", "Rhododendron"), ("Berberis", "Berberis")]},
            {"name": "Bladformer", "plants": [
                ("Flikbladig bok", "Fagus_sylvatica"), ("Flikbladig al", "Alnus_glutinosa"),
                ("Parklind", "Tilia"), ("Pyramidek", "Quercus"), ("Pelarbok", "Fagus")]},
            {"name": "Vintersiluetter", "plants": [
                ("Hängask", "Fraxinus_excelsior"), ("Hängalm", "Ulmus"), ("Hängbok", "Fagus"),
                ("Paraplyalm", "Ulmus_glabra"), ("Pelarbjörk", "Betula")]},
            {"name": "Barktyper", "plants": [
                ("Korkek", "Quercus_suber"), ("Björk bark", "Betula"), ("Tall bark", "Pinus"),
                ("Platan bark", "Platanus"), ("Körsbär bark", "Prunus")]},
            {"name": "Sällsynta svenska", "plants": [
                ("Oxel", "Sorbus_aria"), ("Avenbok", "Carpinus_betulus"), ("Brakved", "Frangula_alnus"),
                ("Benved", "Euonymus_europaeus"), ("Getapel", "Rhamnus_cathartica")]},
            {"name": "Snabbväxande", "plants": [
                ("Hybridpoppel", "Populus"), ("Hybridlärk", "Larix"), ("Douglasgran", "Pseudotsuga"),
                ("Hybridasp", "Populus_tremula"), ("Sitkagran", "Picea_sitchensis")]},
            {"name": "Frukt & nöt", "plants": [
                ("Eldkvarn", "Crataegus"), ("Slån", "Prunus_spinosa"), ("Hagtorn", "Crataegus_monogyna"),
                ("Skogsapel", "Malus_sylvestris"), ("Skogspäron", "Pyrus_pyraster")]},
            {"name": "Hotade arter", "plants": [
                ("Skogslind", "Tilia_cordata"), ("Lundalm", "Ulmus_minor"), ("Ävja", "Najas_flexilis"),
                ("Strandek", "Quercus"), ("Ask", "Fraxinus")]},
            {"name": "Världens träd 1", "plants": [
                ("Baobab", "Adansonia"), ("Drakeblod", "Dracaena_cinnabari"), ("Banyan", "Ficus_benghalensis"),
                ("Kapok", "Ceiba_pentandra"), ("Jakaranda", "Jacaranda")]},
            {"name": "Världens träd 2", "plants": [
                ("Affärsträd", "Delonix_regia"), ("Tamarind", "Tamarindus"), ("Sandelträ", "Santalum_album"),
                ("Kauri", "Agathis_australis"), ("Araukaria", "Araucaria")]},
        ],
    },
    "shrubs": {
        "name": "Buskar",
        "icon": "🌿",
        "description": "Vanliga buskar i trädgården",
        "color": "from-teal-400 to-teal-600",
        "levels": [
            {"name": "Blommande 1", "plants": [
                ("Syren", "Syringa_vulgaris"), ("Forsythia", "Forsythia"), ("Hortensia", "Hydrangea_macrophylla"),
                ("Rhododendron", "Rhododendron"), ("Ros", "Rose")]},
            {"name": "Blommande 2", "plants": [
                ("Liguster", "Ligustrum_vulgare"), ("Måbär", "Ribes_alpinum"), ("Avenbok", "Carpinus_betulus"),
                ("Idegran", "Taxus_baccata"), ("Spirea", "Spiraea")]},
            {"name": "Bärbuskar", "plants": [
                ("Vinbär", "Redcurrant"), ("Krusbär", "Gooseberry"), ("Björnbär", "Blackberry"),
                ("Havtorn", "Hippophae"), ("Aronia", "Aronia")]},
            {"name": "Häckväxter 1", "plants": [
                ("Buxbom", "Buxus"), ("Tuja", "Thuja"), ("Avenbokshäck", "Carpinus_betulus"),
                ("Bokhäck", "Fagus_sylvatica"), ("Häckoxbär", "Cotoneaster")]},
            {"name": "Häckväxter 2", "plants": [
                ("Hagtorn", "Crataegus"), ("Slån", "Prunus_spinosa"), ("Liguster", "Ligustrum"),
                ("Berberis", "Berberis"), ("Pyracantha", "Pyracantha")]},
            {"name": "Rosor 1", "plants": [
                ("Trädgårdsros", "Garden_roses"), ("Klätterros", "Climbing_rose"), ("Buskros", "Rosa_rugosa"),
                ("Äppelros", "Rosa_rubiginosa"), ("Nyponros", "Rosa_canina")]},
            {"name": "Rosor 2", "plants": [
                ("Teeros", "Hybrid_tea_rose"), ("Floribunda", "Floribunda"), ("Rabattros", "Polyantha_rose"),
                ("Marktäckande ros", "Ground_cover_rose"), ("Parkros", "Rosa")]},
            {"name": "Vintergröna 1", "plants": [
                ("Lagerhägg", "Prunus_laurocerasus"), ("Järnek", "Ilex_aquifolium"),
                ("Mahonia", "Mahonia"), ("Skimmia", "Skimmia"), ("Pieris", "Pieris_(plant)")]},
            {"name": "Vintergröna 2", "plants": [
                ("Ljung", "Calluna"), ("Erika", "Erica"), ("Kalmia", "Kalmia"),
                ("Andromeda", "Andromeda_(plant)"), ("Myrten", "Myrtus")]},
            {"name": "Vårblommande 1", "plants": [
                ("Häggmispel", "Amelanchier"), ("Körsbärskornell", "Cornus_mas"),
                ("Kejsarbuske", "Kolkwitzia"), ("Doftschersmin", "Philadelphus"),
                ("Benved", "Euonymus")]},
            {"name": "Vårblommande 2", "plants": [
                ("Trollhassel", "Hamamelis"), ("Vinterblomma", "Chimonanthus"),
                ("Vårginst", "Cytisus"), ("Pimpernöt", "Staphylea"), ("Vårljung", "Erica_carnea")]},
            {"name": "Sommarblommande", "plants": [
                ("Buddleja", "Buddleja"), ("Hibiskus", "Hibiscus_syriacus"), ("Potentilla", "Potentilla"),
                ("Rosenhallon", "Rubus_odoratus"), ("Tamarisk", "Tamarix")]},
            {"name": "Höstfärg 1", "plants": [
                ("Rönnspirea", "Sorbaria"), ("Snöbär", "Symphoricarpos"), ("Rosentry", "Rosa"),
                ("Häggmispel", "Amelanchier_lamarckii"), ("Eldtorn", "Pyracantha")]},
            {"name": "Höstfärg 2", "plants": [
                ("Ginnalalönn", "Acer_ginnala"), ("Kopparlönn", "Acer_griseum"),
                ("Japansk lönn", "Acer_palmatum"), ("Perukbuske", "Cotinus"),
                ("Vingranka", "Vitis_vinifera")]},
            {"name": "Doftande buskar", "plants": [
                ("Schersmin", "Philadelphus"), ("Doftranka", "Lonicera"), ("Lavendel", "Lavandula"),
                ("Citronbuske", "Aloysia_citrodora"), ("Rosmarin", "Salvia_rosmarinus")]},
            {"name": "Torktåliga", "plants": [
                ("Lavendel", "Lavandula"), ("Perovskia", "Perovskia_atriplicifolia"),
                ("Caryopteris", "Caryopteris"), ("Halimium", "Halimium"), ("Cistus", "Cistus")]},
            {"name": "Skuggbuskar", "plants": [
                ("Hortensia", "Hydrangea"), ("Kerria", "Kerria_japonica"), ("Aucuba", "Aucuba"),
                ("Fatsia", "Fatsia"), ("Sarcococca", "Sarcococca")]},
            {"name": "Prydnadsbuskar 1", "plants": [
                ("Sidenbuske", "Kolkwitzia_amabilis"), ("Deutzia", "Deutzia"),
                ("Vägelia", "Weigela"), ("Exochorda", "Exochorda"), ("Ribes", "Ribes_sanguineum")]},
            {"name": "Prydnadsbuskar 2", "plants": [
                ("Kornell", "Cornus"), ("Viburnum", "Viburnum"), ("Cotoneaster", "Cotoneaster"),
                ("Euonymus", "Euonymus"), ("Callicarpa", "Callicarpa")]},
            {"name": "Bärbuskar 2", "plants": [
                ("Blåbär", "Vaccinium_myrtillus"), ("Tranbär", "Vaccinium_oxycoccos"),
                ("Lingon", "Vaccinium_vitis-idaea"), ("Rosenship", "Rosa_canina"),
                ("Fläder", "Sambucus_nigra")]},
            {"name": "Japanska", "plants": [
                ("Japansk quince", "Chaenomeles"), ("Japansk mahonia", "Mahonia_japonica"),
                ("Nandina", "Nandina"), ("Osmanthus", "Osmanthus"),
                ("Japansk skimmia", "Skimmia_japonica")]},
            {"name": "Medelhavet", "plants": [
                ("Oleander", "Nerium"), ("Myrten", "Myrtus_communis"), ("Rosmarin", "Salvia_rosmarinus"),
                ("Lentisk", "Pistacia_lentiscus"), ("Kaprifol", "Lonicera_caprifolium")]},
            {"name": "Exotiska", "plants": [
                ("Kamelbuske", "Camellia_japonica"), ("Fothergilla", "Fothergilla"),
                ("Enkianthus", "Enkianthus"), ("Clethra", "Clethra"), ("Itea", "Itea")]},
            {"name": "Nytta & nytta", "plants": [
                ("Humle", "Humulus"), ("Vinranka", "Vitis"), ("Kiwi", "Actinidia"),
                ("Passionsblomma", "Passiflora"), ("Aktinidia", "Actinidia_deliciosa")]},
            {"name": "Taggiga", "plants": [
                ("Hagtorn", "Crataegus_monogyna"), ("Berberis", "Berberis_thunbergii"),
                ("Eldtorn", "Pyracantha_coccinea"), ("Slån", "Prunus_spinosa"),
                ("Stickros", "Rosa_pimpinellifolia")]},
            {"name": "Marktäckare", "plants": [
                ("Gaultheria", "Gaultheria"), ("Hypericum", "Hypericum_calycinum"),
                ("Stephanandra", "Stephanandra"), ("Krypvide", "Salix_repens"),
                ("Krypoxbär", "Cotoneaster_dammeri")]},
            {"name": "Vinterintresse", "plants": [
                ("Rödkornell", "Cornus_sanguinea"), ("Gulkornell", "Cornus_sericea"),
                ("Häxal", "Hamamelis_mollis"), ("Viburnum bodnantense", "Viburnum"),
                ("Jasmin vinter", "Jasminum_nudiflorum")]},
            {"name": "Kompakta", "plants": [
                ("Dvärgmandel", "Prunus_tenella"), ("Liten syren", "Syringa_meyeri"),
                ("Dvärgspirea", "Spiraea_japonica"), ("Dvärgberberis", "Berberis"),
                ("Dvärgrododendron", "Rhododendron")]},
            {"name": "Expert 1", "plants": [
                ("Disanthus", "Disanthus"), ("Heptacodium", "Heptacodium"), ("Lindera", "Lindera"),
                ("Zenobia", "Zenobia_(plant)"), ("Leycesteria", "Leycesteria")]},
            {"name": "Expert 2", "plants": [
                ("Abelia", "Abelia"), ("Clerodendrum", "Clerodendrum"), ("Davidia", "Davidia"),
                ("Stewartia", "Stewartia"), ("Styrax", "Styrax")]},
        ],
    },
    "annuals": {
        "name": "Sommarblommor",
        "icon": "🌻",
        "description": "Ettåriga blommor för sommaren",
        "color": "from-amber-400 to-orange-500",
        "levels": [
            {"name": "Klassiker 1", "plants": [
                ("Tagetes", "Tagetes"), ("Petunia", "Petunia"), ("Solros", "Sunflower"),
                ("Ringblomma", "Calendula"), ("Lobelia", "Lobelia")]},
            {"name": "Klassiker 2", "plants": [
                ("Dahlia", "Dahlia"), ("Zinnia", "Zinnia"), ("Luktärt", "Sweet_pea"),
                ("Pensé", "Pansy"), ("Cosmos", "Cosmos_bipinnatus")]},
            {"name": "Klassiker 3", "plants": [
                ("Amarant", "Amaranth"), ("Lejonmun", "Antirrhinum"), ("Verbena", "Verbena"),
                ("Praktnejlika", "Dianthus_barbatus"), ("Salvia", "Salvia_splendens")]},
            {"name": "Balkongblommor 1", "plants": [
                ("Pelargon", "Pelargonium"), ("Surfinior", "Calibrachoa"), ("Nemesia", "Nemesia"),
                ("Bacopa", "Bacopa_monnieri"), ("Bidens", "Bidens_(plant)")]},
            {"name": "Balkongblommor 2", "plants": [
                ("Fuchsia", "Fuchsia"), ("Begonia", "Begonia"), ("Impatiens", "Impatiens"),
                ("Tusensköna", "Bellis_perennis"), ("Ageratum", "Ageratum")]},
            {"name": "Balkongblommor 3", "plants": [
                ("Diascia", "Diascia"), ("Osteospermum", "Osteospermum"), ("Gazania", "Gazania"),
                ("Lantana", "Lantana"), ("Scaevola", "Scaevola_(plant)")]},
            {"name": "Utplanteringsblommor 1", "plants": [
                ("Trädgårdsbégonia", "Begonia_semperflorens"), ("Lysblomma", "Lobularia_maritima"),
                ("Lejongap", "Antirrhinum_majus"), ("Riddarsporre", "Consolida"),
                ("Blåklint", "Centaurea_cyanus")]},
            {"name": "Utplanteringsblommor 2", "plants": [
                ("Krasse", "Tropaeolum"), ("Morgongloria", "Ipomoea"), ("Eldkrasse", "Tropaeolum_majus"),
                ("Klockranka", "Cobaea"), ("Vinda", "Convolvulus")]},
            {"name": "Utplanteringsblommor 3", "plants": [
                ("Aster", "Callistephus"), ("Gomphrena", "Gomphrena"), ("Celosia", "Celosia"),
                ("Cleome", "Cleome"), ("Tithonia", "Tithonia")]},
            {"name": "Snittblommor 1", "plants": [
                ("Limonium", "Limonium"), ("Delphinium", "Consolida_ajacis"), ("Lathyrus", "Lathyrus"),
                ("Scabiosa", "Scabiosa"), ("Nigella", "Nigella")]},
            {"name": "Snittblommor 2", "plants": [
                ("Goddetia", "Clarkia"), ("Matthiola", "Matthiola"), ("Coreopsis", "Coreopsis"),
                ("Ammi", "Ammi_majus"), ("Orlaya", "Orlaya_grandiflora")]},
            {"name": "Snittblommor 3", "plants": [
                ("Dill", "Dill"), ("Eucalyptus", "Eucalyptus"), ("Gypsophila", "Gypsophila"),
                ("Solidago", "Solidago"), ("Eryngium", "Eryngium")]},
            {"name": "Doftande 1", "plants": [
                ("Luktärta", "Lathyrus_odoratus"), ("Reseda", "Reseda_odorata"), ("Heliotrope", "Heliotropium"),
                ("Doftviol", "Viola_odorata"), ("Tobaksblomma", "Nicotiana")]},
            {"name": "Doftande 2", "plants": [
                ("Nattljus", "Oenothera"), ("Mirabilis", "Mirabilis_jalapa"), ("Nattviol", "Hesperis_matronalis"),
                ("Doftpelargon", "Pelargonium_graveolens"), ("Lavendel", "Lavandula")]},
            {"name": "Ettåriga gräs", "plants": [
                ("Harsvans", "Lagurus_ovatus"), ("Darrgräs", "Briza"), ("Borstgräs", "Setaria"),
                ("Fjädergräs", "Stipa_pennata"), ("Pärlgräs", "Coix_lacryma-jobi")]},
            {"name": "Solälskande", "plants": [
                ("Portulaka", "Portulaca_grandiflora"), ("Isbegonia", "Dorotheanthus"),
                ("Sammetblomma", "Salpiglossis"), ("Rudbeckia", "Rudbeckia_hirta"),
                ("Helianthus", "Helianthus")]},
            {"name": "Skuggväxter", "plants": [
                ("Flitiga Lisa", "Impatiens_walleriana"), ("Begonia", "Begonia_semperflorens"),
                ("Mimulus", "Erythranthe"), ("Torenia", "Torenia"), ("Browallia", "Browallia")]},
            {"name": "Klättrande ettåriga", "plants": [
                ("Luktärt", "Lathyrus_odoratus"), ("Svartöga", "Thunbergia_alata"),
                ("Kanarieblomma", "Tropaeolum_peregrinum"), ("Humle", "Humulus_japonicus"),
                ("Ipomoea", "Ipomoea_purpurea")]},
            {"name": "Vildblommor 1", "plants": [
                ("Vallmo", "Papaver_rhoeas"), ("Blåklint", "Centaurea_cyanus"),
                ("Prästkrage", "Leucanthemum_vulgare"), ("Klöver", "Trifolium"),
                ("Kamomill", "Matricaria_chamomilla")]},
            {"name": "Vildblommor 2", "plants": [
                ("Blåeld", "Echium_vulgare"), ("Rödklöver", "Trifolium_pratense"),
                ("Gullviva", "Primula_veris"), ("Ängsvädd", "Succisa_pratensis"),
                ("Kungsljus", "Verbascum")]},
            {"name": "Exotiska 1", "plants": [
                ("Anagallis", "Lysimachia_arvensis"), ("Felicia", "Felicia"), ("Dimorphotheca", "Dimorphotheca"),
                ("Ursinia", "Ursinia"), ("Arctotis", "Arctotis")]},
            {"name": "Exotiska 2", "plants": [
                ("Cuphea", "Cuphea"), ("Pentas", "Pentas"), ("Mandevilla", "Mandevilla"),
                ("Dipladenia", "Mandevilla_sanderi"), ("Tibouchina", "Tibouchina")]},
            {"name": "Höstblommande", "plants": [
                ("Höstaster", "Callistephus_chinensis"), ("Solros", "Helianthus_annuus"),
                ("Dahlia", "Dahlia"), ("Chrysantemum", "Chrysanthemum"), ("Amarant", "Amaranthus")]},
            {"name": "Torktåliga", "plants": [
                ("Isört", "Delosperma"), ("Portulaka", "Portulaca"), ("Vaxblomma", "Cerinthe"),
                ("Lavatéra", "Lavatera"), ("Dimorfoteka", "Dimorphotheca")]},
            {"name": "Matbara blommor", "plants": [
                ("Ringblomma", "Calendula_officinalis"), ("Penséer", "Viola_tricolor"),
                ("Krasseblomma", "Tropaeolum"), ("Fläder", "Sambucus_nigra"),
                ("Lavendel", "Lavandula_angustifolia")]},
            {"name": "Fjärilsväxter", "plants": [
                ("Buddleja", "Buddleja_davidii"), ("Verbena", "Verbena_bonariensis"),
                ("Zinnia", "Zinnia_elegans"), ("Tagetes", "Tagetes_patula"),
                ("Sedum", "Sedum_spectabile")]},
            {"name": "Fröställningar", "plants": [
                ("Vallmo kapsel", "Papaver_somniferum"), ("Nigella fröhus", "Nigella_damascena"),
                ("Luffa", "Luffa"), ("Solros", "Helianthus"), ("Penningblad", "Lunaria")]},
            {"name": "Ampelblommor", "plants": [
                ("Hängpetunia", "Petunia"), ("Hänglobelia", "Lobelia_erinus"),
                ("Hängverbena", "Verbena"), ("Hängfuchsia", "Fuchsia"),
                ("Hängbegonia", "Begonia_boliviensis")]},
            {"name": "Expert 1", "plants": [
                ("Nicandra", "Nicandra"), ("Malope", "Malope"), ("Moluccella", "Moluccella"),
                ("Nolana", "Nolana"), ("Emilia", "Emilia_(plant)")]},
            {"name": "Expert 2", "plants": [
                ("Schizanthus", "Schizanthus"), ("Tweedia", "Tweedia_caerulea"),
                ("Trachelium", "Trachelium"), ("Ageratum", "Ageratum_houstonianum"),
                ("Xeranthemum", "Xeranthemum")]},
        ],
    },
}


def fetch_images(plant_titles):
    """Fetch Wikipedia images for a batch of titles."""
    results = {}
    titles_list = list(set(plant_titles))

    for i in range(0, len(titles_list), 50):
        batch = titles_list[i:i+50]
        titles_str = "|".join(batch)
        url = (
            f"https://en.wikipedia.org/w/api.php?action=query"
            f"&titles={urllib.parse.quote(titles_str)}"
            f"&prop=pageimages&piprop=thumbnail&pithumbsize=400&format=json&redirects=1"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "PlantLearnerApp/1.0"})
        try:
            resp = urllib.request.urlopen(req)
            data = json.loads(resp.read())
        except Exception as e:
            print(f"  Error fetching batch: {e}", file=sys.stderr)
            time.sleep(2)
            continue

        pages = data.get("query", {}).get("pages", {})
        normalized = {n["to"]: n["from"] for n in data.get("query", {}).get("normalized", [])}
        redirects = {r["to"]: r["from"] for r in data.get("query", {}).get("redirects", [])}

        for pid, page in pages.items():
            title = page.get("title", "")
            thumb = page.get("thumbnail", {}).get("source", "")
            if thumb:
                original = title
                if title in redirects:
                    original = redirects[title]
                if original in normalized:
                    original = normalized[original]
                path = thumb.replace("https://upload.wikimedia.org", "").replace("/500px-", "/400px-")
                results[original] = path

        time.sleep(0.5)

    return results


def generate_js(image_map):
    """Generate the plants.js file content."""
    lines = [
        '// Växtdatabas med kategorier, nivåer och bilder',
        '// Auto-genererad med Wikipedia API-bilder',
        '',
        'function img(path) {',
        '  return `/wiki-img${path}`;',
        '}',
        '',
        'export const categories = [',
    ]

    for cat_id, cat in CATEGORIES.items():
        lines.append('  {')
        lines.append(f'    id: {json.dumps(cat_id)},')
        lines.append(f'    name: {json.dumps(cat["name"])},')
        lines.append(f'    icon: {json.dumps(cat["icon"])},')
        lines.append(f'    description: {json.dumps(cat["description"])},')
        lines.append(f'    color: {json.dumps(cat["color"])},')
        lines.append('    levels: [')

        for level_idx, level in enumerate(cat["levels"]):
            lines.append('      {')
            lines.append(f'        id: {level_idx + 1},')
            lines.append(f'        name: {json.dumps(level["name"])},')
            lines.append('        plants: [')

            for sv_name, en_title in level["plants"]:
                img_path = image_map.get(en_title, "")
                if img_path:
                    lines.append(f'          {{ name: {json.dumps(sv_name)}, image: img({json.dumps(img_path)}) }},')
                else:
                    lines.append(f'          {{ name: {json.dumps(sv_name)}, image: "" }},')

            lines.append('        ],')
            lines.append('      },')

        lines.append('    ],')
        lines.append('  },')

    lines.append('];')
    lines.append('')
    lines.append('export function getAllPlantsInCategory(categoryId) {')
    lines.append('  const category = categories.find(c => c.id === categoryId);')
    lines.append('  if (!category) return [];')
    lines.append('  return category.levels.flatMap(level => level.plants);')
    lines.append('}')
    lines.append('')
    lines.append('export function getPlantsForLevel(categoryId, levelId) {')
    lines.append('  const category = categories.find(c => c.id === categoryId);')
    lines.append('  if (!category) return [];')
    lines.append('  const level = category.levels.find(l => l.id === levelId);')
    lines.append('  return level ? level.plants : [];')
    lines.append('}')

    return '\n'.join(lines)


if __name__ == '__main__':
    # Collect all unique Wikipedia titles
    all_titles = []
    for cat in CATEGORIES.values():
        for level in cat["levels"]:
            for sv_name, en_title in level["plants"]:
                all_titles.append(en_title)

    unique_titles = list(set(all_titles))
    print(f"Fetching images for {len(unique_titles)} unique plants...", file=sys.stderr)

    image_map = fetch_images(unique_titles)
    found = sum(1 for t in unique_titles if t in image_map)
    print(f"Found images for {found}/{len(unique_titles)} plants", file=sys.stderr)

    js_content = generate_js(image_map)
    print(js_content)
