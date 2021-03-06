/* Sleep for ms many milliseconds. */
function sleep(ms)
{
	return new Promise(resolve => setTimeout(resolve, ms));
}

/* Typewriter function taking an object to write to, text to write, and speed
   (latency) in ms between letters written. Writes one character at a time. */
async function typewriter(object, text, speed)
{
	for (let i = 0; i <= text.length; i++)
	{
		await sleep(speed);
		object.text(text.slice(0, i));
	}
}

/* Same as typewriter, but wait a delay in ms before writing. This is akin to
   a hibernation period before text begins to write. */
async function typewriter_d(object, text, speed, delay)
{
	await sleep(delay);
	typewriter(object, text, speed);
}

/* typewriter, but in reverse. */
async function rtypewriter(object, speed)
{
	while (object.text().length > 0)
	{
		await sleep(speed);
		object.text(object.text().slice(0, object.text().length-1));
	}
}

/* typewriter_d, but in reverse. */
async function rtypewriter_d(object, speed, delay)
{
	await sleep(delay);
	rtypewriter(object, speed);
}
