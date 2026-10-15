function status(request, response) {
  response.status(200).json({ chave: "Desenvolvimento aplicativo Foveli" });
}

export default status;
