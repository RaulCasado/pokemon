const Home = () => {
return (
	<div className="container mx-auto mt-8 px-4">
		<h1 className="text-4xl font-bold text-center text-red-500">
			¡Bienvenido al Quiz de Pokémon!
		</h1>
		<p className="mt-4 text-lg text-gray-700 text-center">
			¿Eres un verdadero maestro Pokémon? Demuestra tus conocimientos en este
			emocionante quiz basado en el mundo Pokémon. Responde preguntas sobre
			tipos, movimientos, generaciones y mucho más.
		</p>
		<p className="mt-2 text-lg text-gray-700 text-center">
			Puedes jugar en modo solitario para superar tu propio récord, o
			desafiar a tus amigos en el modo multijugador.
		</p>
		<div className="mt-8 flex justify-center">
			<img
				src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
				alt="Pikachu"
				className="w-32 h-32"
			/>
		</div>
	</div>
);
};

export default Home;
