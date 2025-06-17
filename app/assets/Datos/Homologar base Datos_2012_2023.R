datos = sf::read_sf("app/assets/Datos/shp/Historicos_Acciones.shp")

base = readxl::read_xlsx("app/assets/Datos/DATOS_2012_2023.xlsx")

names(base)



interes = base |>  
  dplyr::select(`Arsenico
mg/L`:`Temperatura 
°C`) 
interes = interes |>  dplyr::select(-`Cloro residual 
mg/L`)
interes = names(interes)

interes = gsub(x = interes, pattern ="\n.*", replacement = "") |> stringr::str_trim()



municipal = datos
municipal = municipal |> 
  dplyr::mutate(Arsenico = sample(1:1000,84, replace=F),
                Bario = sample(1:1000,84, replace=F),
                Cadmio = sample(1:1000,84, replace=F),
                Cobre = sample(1:1000,84, replace=F),
                Hierro = sample(1:1000,84, replace=F),
                Manganeso = sample(1:1000,84, replace=F),
                Plomo = sample(1:1000,84, replace=F),
                Zinc = sample(1:1000,84, replace=F),
                Dureza_Total = sample(1:1000,84, replace=F),
                Fluoruros = sample(1:1000,84, replace=F),
                Nitratos = sample(1:1000,84, replace=F),
                Nitritos = sample(1:1000,84, replace=F),
                pH = sample(1:1000,84, replace=F),
                SDT = sample(1:1000,84, replace=F),
                Sulfatos = sample(1:1000,84, replace=F),
                Cloro_Total = sample(1:1000,84, replace=F),
                Conductividad = sample(1:1000,84, replace=F),
                Temperatura = sample(1:1000,84, replace=F),
                )



promedio = base |> 
  dplyr::mutate(Municipio = stringr::str_to_title(Municipio),
                Municipio = iconv(x = Municipio, from = "UTF-8", to = "ASCII//TRANSLIT"),
                Municipio = stringr::str_trim(Municipio)) |> 
  dplyr::select(Año, Municipio, `Cloro residual 
mg/L`) |> 
  dplyr::mutate(Id = paste0(Municipio, "_",Año))

promedio = promedio |> 
  dplyr::group_by(Id) |> 
  dplyr::summarise(promedio = max(as.numeric(`Cloro residual 
mg/L`),na.rm = T))






sf::write_sf(municipal, "app/assets/Datos/shp/Municipal_prueba.shp")







































####################
## Homologar base ##
####################



datos = readxl::read_xlsx("app/assets/Datos/DATOS_2012_2023.xlsx") 

mun = sf::read_sf("../../Importantes_documentos_usar/Municipios/municipiosjair.shp")
mun = mun |>  
  dplyr::select(CVEGEO, NOM_MUN) |> 
  dplyr::mutate(Municipio = NOM_MUN,
                Municipio = stringr::str_to_title(Municipio),
                Municipio = iconv(x = Municipio, from = "UTF-8", to = "ASCII//TRANSLIT"),
                Municipio = stringr::str_trim(Municipio)
                ) |> 
  sf::st_drop_geometry()

datos = datos |> 
  dplyr::mutate(Municipio = stringr::str_to_title(Municipio),
                Municipio = iconv(x = Municipio, from = "UTF-8", to = "ASCII//TRANSLIT"),
                Municipio = stringr::str_trim(Municipio)) 

unicos = datos$Municipio |>  unique()
unicos[which(!unicos %in% mun$Municipio)]

datos = datos  |> 
  dplyr::mutate(Municipio = dplyr::case_when(
    Municipio == "San Agustin Tlaxiaca 2017" ~ "San Agustin Tlaxiaca",
    Municipio == "Santago Tulantepec" ~ "Santiago Tulantepec De Lugo Guerrero",
    Municipio == "San Agustin Tlaxiaca 2019" ~ "San Agustin Tlaxiaca",
    Municipio == "San Aguatin Tlaxiaca" ~ "San Agustin Tlaxiaca",
    Municipio == "Zacualtipan" ~ "Zacualtipan De Angeles",
    Municipio == "Tepehuacan" ~ "Tepehuacan De Guerrero",
    Municipio == "Huasca" ~ "Huasca De Ocampo",
    Municipio == "Cuautepec" ~ "Cuautepec De Hinojosa",
    Municipio == "Santiago Tulantepec (Chignahuapan)" ~ "Santiago Tulantepec De Lugo Guerrero",
    Municipio == "Mixquiahuala" ~ "Mixquiahuala De Juarez",
    Municipio == "Huejutla" ~ "Huejutla De Reyes",
    Municipio == "Atitalaquia (Atotonilco De Tula)" ~ "Atitalaquia",
    Municipio == "Jacala" ~ "Jacala De Ledezma",
    Municipio == "Agua Blanca" ~ "Agua Blanca De Iturbide",
    Municipio == "Zacualtipan Angeles" ~ "Zacualtipan De Angeles",
    Municipio == "Villas De Tezontepec" ~ "Villa De Tezontepec",
    Municipio == "Tepeji Del Rio" ~ "Tepeji Del Rio De Ocampo",
    Municipio == "Santiago Tulantepec" ~ "Santiago Tulantepec De Lugo Guerrero",
    Municipio == "Molango" ~ "Molango De Escamilla",
    Municipio == "Juarez De Hidalgo" ~ "Juarez Hidalgo",
    TRUE ~ Municipio
    ))

colnames(mun)[1] = "CVEGEO_MUN"

datos = merge(x = datos, y = mun, by = "Municipio", all.x = T)


loc = sf::read_sf("../../Importantes_documentos_usar/Localidades/shp1/13l.shp")
loc = loc |>  
  dplyr::select(CVEGEO, NOMGEO) |> 
  dplyr::mutate(Localidad = NOMGEO,
                Localidad = stringr::str_to_title(Localidad),
                Localidad = iconv(x = Localidad, from = "UTF-8", to = "ASCII//TRANSLIT"),
                Localidad = stringr::str_trim(Localidad),
                Id = paste0(substr(x = CVEGEO, start = 1, stop = 5), "_", Localidad)
  ) |>  sf::st_drop_geometry()


datos = datos |> 
  dplyr::mutate(Localidad = stringr::str_to_title(Localidad),
                Localidad = iconv(x = Localidad, from = "UTF-8", to = "ASCII//TRANSLIT"),
                Localidad = stringr::str_trim(Localidad),
                Id = paste0(CVEGEO_MUN, "_", Localidad)) 

unicos = datos$Id |>  unique()
unicos[which(!unicos %in% loc$Id)]


datos = datos  |> 
  dplyr::mutate(Municipio = dplyr::case_when(
    Id == "13001_Colonia 28 De Mayo" ~ "13001_28 de Mayo (Santa Rosa) [Colonia]",
    Id == "13001_San Bartolo El Llano" ~ "13001_San Bartolo (El Llano)",
    Id == "13001_Col. 28 De Mayo (Santa Rosa)" ~ "13001_28 de Mayo (Santa Rosa) [Colonia]",
    Id == "13001_El Sabino" ~ "13001_El Sabino (La Barranca)",
    
    Id == "13002_Barrio Tlatzintla" ~ "13002_Tlatzintla",
    Id == "13002_Barrio Tlaltegco" ~ "13002_Tlaltegco (Venta Quemada)",
    Id == "13002_Apapaxtla El Grande" ~ "13002_Apapaxtla El Grande (Altamira)",
    Id == "13002_Tlamimolpan" ~ "13002_Tlamimilolpa",
    TRUE ~ Id
  ))




write.csv(loc,"app/assets/Datos/Localidad_basarse.csv", row.names = F, fileEncoding = "latin1")
