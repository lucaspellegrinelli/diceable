<svelte:head>
	<script src="https://cdn.socket.io/4.6.0/socket.io.min.js" integrity="sha384-c79GN5VsunZvi+Q/WObgk2in0CbZsHnjEqvFxC5DxHn9lTfNce2WW6h2pH6u/kF+" crossorigin="anonymous"></script>
</svelte:head>

<script>
	// @ts-nocheck
	import { getDicePositions } from '$lib/dicePositionCalculator';
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';

	export let data;
	const userToken = data.user;

	const hideDelay = 8000;

	const animationFrames = 28;
	const animationDelay = 50;

	const sizeFactor = 0.7;

	const imgWidth = Math.round(550 * sizeFactor);
	const imgHeight = Math.round(475 * sizeFactor);
	const diceWidth = Math.round(460 * sizeFactor);
	const diceHeight = Math.round(443 * sizeFactor);
	const screenWidth = 1920;
	const screenHeight = 1080;
	const marginX = 10;
	const marginY = 10;

	onMount(() => {
		let hideTimeout = null;

		const updateContent = async (rolls, sides, palette, effect) => {
			clearContent();

			const numberDice = rolls.length;

			palette.unshift(palette.pop());
			const parsedPalette = JSON.stringify(
				palette.map((diceSkin, i) => ({ name: diceSkin, number: i }))
			);

			const queryItems = [];
			queryItems.push(`number=${numberDice}`);
			queryItems.push(`palette=${parsedPalette}`);
			queryItems.push(`sides=${sides}`);
			if (effect) {
				queryItems.push(`effect=${effect}`);
			}
			const query = queryItems.join('&');

			const fetchUrl = `/api/assets?${query}`;
			const response = await fetch(fetchUrl);
			const result = await response.json();

			const effectUrl = result.effect;
			const diceUrls = result.dice;

			const startDiceAnimation = (targetNumber, dom) => {
				let frame = 0;
				let loopTimeout = null;

				const animate = () => {
					const isLast = frame === animationFrames - 1;
					if (frame < animationFrames) {
						const diceNumber = isLast ? targetNumber : Math.floor(Math.random() * palette.length);
						dom.style.display = 'block';
						dom.src = diceUrls[diceNumber];
					}

					frame += 1;

					if (frame >= animationFrames) {
						clearInterval(loopTimeout);
					}
				};

				loopTimeout = setInterval(animate, animationDelay);

				clearTimeout(hideTimeout);
				hideTimeout = setTimeout(clearContent, hideDelay);
			};

			const preloadImages = [];
			for (let i = 0; i < palette.length; i++) {
				const preloadImage = new Image();
				preloadImage.src = diceUrls[i];
				preloadImages.push(preloadImage);
			}

			const dicePositions = getDicePositions(
				rolls.length,
				imgWidth,
				imgHeight,
				diceWidth,
				diceHeight,
				screenWidth,
				screenHeight,
				marginX,
				marginY
			);

			const allImgDoms = [];
			const imgContainer = document.getElementById('dice');
			for (let i = 0; i < rolls.length; i++) {
				const imgDom = document.createElement('img');
				const x = dicePositions[i][0] - 3;
				const y = dicePositions[i][1] - 3;
				imgDom.id = `roll-img-${i}`;
				imgDom.src = '';
				imgDom.style.position = 'absolute';
				imgDom.style.top = '' + y + 'px';
				imgDom.style.left = '' + x + 'px';
				imgDom.style.width = `${imgWidth}px`;
				imgDom.style.height = `${imgHeight}px`;
				imgDom.style.display = 'none';
				allImgDoms.push(imgDom);
				imgContainer.appendChild(imgDom);
			}

			let diceSkinLoadedCount = 0;
			let effectLoaded = !effect;

			const onEverythingLoaded = () => {
				if (effect) {
					const video = document.getElementById('roll-video');
					video.play();
				}

				for (let i = 0; i < rolls.length; i++) {
					const roll = rolls[i] % palette.length;
					startDiceAnimation(roll, allImgDoms[i]);
				}
			};

			const onAssetLoaded = () => {
				if (diceSkinLoadedCount === palette.length && effectLoaded) {
					onEverythingLoaded();
				}
			};

			const onDiceSkinLoad = () => {
				diceSkinLoadedCount += 1;
				onAssetLoaded();
			};

			const onEffectLoad = () => {
				effectLoaded = true;
				onAssetLoaded();
			};

			for (let i = 0; i < preloadImages.length; i++) {
				preloadImages[i].onload = onDiceSkinLoad;
			}

			if (effect) {
				const video = document.getElementById('roll-video');
				const source = document.getElementById('roll-source');

				video.pause();
				source.src = effectUrl;
				video.load();

				video.oncanplaythrough = onEffectLoad;
			}
		};

		const clearContent = () => {
			const imgContainer = document.getElementById('dice');
			const video = document.getElementById('roll-video');
			const source = document.getElementById('roll-source');

			imgContainer.innerHTML = '';
			source.src = '';
			video.load();
		};

		const handleMessage = (parsedMessage) => {
			if (parsedMessage.user_id === userToken) {
				const rolls = parsedMessage.rolls;
				const sides = parsedMessage.sides;
				const palette = parsedMessage.palette;
				const effect = parsedMessage.effect;
				updateContent(rolls, sides, palette, effect);
			}
		};

		const socket = io(env.PUBLIC_SOCKETIO_URL, {
			withCredentials: true,
		});

		socket.on('connect', () => {
			console.log('Connected to socket.io server. My ID:', socket.id);
		});

		socket.on('disconnect', () => {
			console.log('Disconnected from socket.io server');
		});

		socket.on('connect_error', (err) => {
			console.log('Connection error', err);
		});

		socket.on('connect_timeout', (err) => {
			console.log('Connection timeout', err);
		});

		socket.on('error', (err) => {
			console.log('Socket.io error', err);
		});

		socket.on('roll', (data) => {
			console.log('Received "roll" with data:', data);
			handleMessage(data);
		});
	});
</script>

<div id="dice" />

<div id="effect">
	<video id="roll-video" muted>
		<source src="" id="roll-source" type="video/mp4" />
	</video>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		overflow: hidden;
		background-color: transparent;
	}

	#dice {
		width: 1920px;
		height: 1080px;
	}

	#effect {
		width: 1920px;
		height: 1080px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
