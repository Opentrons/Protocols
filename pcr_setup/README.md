# Custom PCR Setup

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Molecular Biology
	* DNA
* Sample Prep
	* PCR

## Description
Generate and download a custom PCR protocol by following the setup steps below, tailored to your needs.

<iframe id="embedded-app" src="https://s3.amazonaws.com/opentrons-parametric-protocols/PCRQuestions.html" style="width: 100%; border: none;">
	<p>Your browser does not support iframes. Please try again with a more up-to-date browser.</p>
</iframe>

<script>
	console.log('hello from markdown.');

	// Create IE + others compatible event handler
	// Listen to message from child window
	window.addEventListener("message", function(e) {
		var origin = e.origin || e.originalEvent.origin; // Chrome support (uses originalEvent)

	  console.log('parent received message!:  ', {data: e.data, origin, e});

		// Set iframe height
		document.getElementById("embedded-app").height = parseInt(e.data, 10) * 1.1;
	}, false);
</script>

### Time Estimate
Varies depending on your settings

### Robot
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT PRO](https://opentrons.com/ot-one-pro)

### Modules

### Reagents
* Samples
* Pre-mixed Master Mixes

## Process

### Additional Notes



###### Internal
