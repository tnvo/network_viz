
var PieChart = function (data, attributes) {
	this.data = data;
	this.attributes = attributes;
	this.draw();
};

// The PieChart prototype exposing the functionality
PieChart.prototype = {

	// set colors to data elements if they weren't passed
	initColors: function () {
		var colors = [ "#c53333", "#2f90f9", "#0dc9a8", "#4e4ef8", "#c2fffd", "#f6ca11", "#90f92f", "#85929e",  "#fb7676"];

		for (var i = 0; i < this.data.length; i++) {
			this.data[i].color = colors[i];
		}
	},

	// draw the pie chart
	draw: function () {
		// create the canvas if it doesn't exist
		this.canvas = this.canvas || this.createCanvas();
		this.resizeCanvas();

		this.initColors();

		var width = parseInt(this.attributes.width),
			height = parseInt(this.attributes.height);

		// set canvas properties
		var ctx = this.canvas.getContext("2d");
		ctx.font = "20px Courier";

		var lastend = 0;

		for (var i = 0; i < this.data.length; i++) {
			ctx.fillStyle = this.data[i].color;
			ctx.beginPath();

			var point = height / 2;

			ctx.moveTo(point, point);
			ctx.arc(point + 1, point + 1, point - 2, lastend, lastend + (Math.PI * 2 * (this.data[i].value / 100)), false);

			ctx.fill();

			// write the text
			ctx.fillText(this.data[i].name, height + (height/10), (i + 1) * 30);
			ctx.stroke();

			lastend += Math.PI * 2 * (this.data[i].value / 100);
		}
	},

	// create the canvas DOM object and add it to the body, return it
	createCanvas: function () {
		var canvas = document.createElement("canvas");

		this.attributes = this.attributes || {};

		this.attributes.width = this.attributes.size || "320px";
		this.attributes.height = this.attributes.size || "320px";

		for (attribute in this.attributes) {
			canvas.setAttribute(attribute, this.attributes[attribute]);
		}

		document.body.appendChild(canvas);

		return canvas;
	},

	// resize the canvas width to account for legend text
	resizeCanvas: function () {
		var largest = 0;
		var height = parseInt(this.attributes.height);

		for (var i = 0; i < this.data.length; i++) {
			if (this.data[i].name.length > largest) {
				largest = this.data[i].name.length;
			}
		}

		var width = height + (largest * 12) + (height / 10);

		this.canvas.setAttribute("width", width + "px");
	}
};
