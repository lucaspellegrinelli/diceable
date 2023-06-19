<script>
	// @ts-nocheck
	import { io } from '$lib/webSocketConnection';
	import { getDicePositions } from '$lib/dicePositionCalculator';
	import { onMount } from 'svelte';

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

		const updateContent = async (rolls, palette, effect) => {
			clearTimeout(hideTimeout);
			clearContent();

			const numberDice = rolls.length;

			const parsedPalette = JSON.stringify(
				palette.map((diceSkin, i) => ({ name: diceSkin, number: i }))
			);

			const queryItems = [];
			queryItems.push(`number=${numberDice}`);
			queryItems.push(`palette=${parsedPalette}`);
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

			if (effect) {
				const video = document.getElementById('roll-video');
				const source = document.getElementById('roll-source');

				video.pause();
				source.src = effectUrl;
				video.load();

				video.oncanplaythrough = () => {
					video.play();
					for (let i = 0; i < rolls.length; i++) {
						const roll = rolls[i] % palette.length;
						startDiceAnimation(roll, allImgDoms[i]);
					}
				};
			} else {
				preloadImages[preloadImages.length - 1].onload = () => {
					for (let i = 0; i < rolls.length; i++) {
						const roll = rolls[i] % palette.length;
						startDiceAnimation(roll, allImgDoms[i]);
					}
				};
			}

			hideTimeout = setTimeout(clearContent, hideDelay);
		};

		const clearContent = () => {
			const imgContainer = document.getElementById('dice');
			const video = document.getElementById('roll-video');
			const source = document.getElementById('roll-source');

			imgContainer.innerHTML = '';
			source.src = '';
			video.load();
		};

		io.on('rolls', (message) => {
			if (message.user_id === userToken) {
				const rolls = message.rolls;
				const palette = message.palette;
				const effect = message.effect;
				updateContent(rolls, palette, effect);
			}
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
