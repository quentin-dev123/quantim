bg = {
  Français: "#004164",
  SVT: "#006412ff",
  Maths: "#004164",
  Espagnol: "#643100ff",
  Tecnologie: "#330064ff",
  PhysiqueChimie: "#636400ff", // Attention Physique-Chimie = PhysiqueChimie
  EPS: "#070064ff",
  Artsplastique: "#540064ff", // Attention Arts plastiques = Artsplastique
  Histoiregéo: "#64002dff", // Attention Histoire-géo = Histoiregéo
  Anglais: "#1a6400ff",
  Autre: "#006452ff",
}

function remove_space_hyphen(text) {
  text = text.replaceAll(" ", "");
  text = text.replaceAll("-", "");
  return text
}
