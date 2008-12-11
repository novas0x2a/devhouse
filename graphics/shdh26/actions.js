//Global Variables
var niceforms = document.getElementsByTagName('form'); var inputs = new Array(); var labels = new Array(); var radios = new Array(); var radioLabels = new Array(); var checkboxes = new Array(); var checkboxLabels = new Array(); var texts = new Array(); var textareas = new Array(); var selects = new Array(); var selectText = "please select"; var agt = navigator.userAgent.toLowerCase(); this.ie = ((agt.indexOf("msie") != -1) && (agt.indexOf("opera") == -1)); var hovers = new Array(); var buttons = new Array(); var isMac = new RegExp('(^|)'+'Apple'+'(|$)');

var imagesPath = "images/";

//Initialization function - if you have any other 'onload' functions, add them here
function init() {
	if(!document.getElementById) {return false;}
	preloadImages();
	getElements();
	separateElements();
	if(!isMac.test(navigator.vendor)) {
		replaceTexts();
		replaceTextareas();
		buttonHovers();
	}
}

function preloadImages() {
	preloads = new Object();
	preloads[0] = new Image(); preloads[0].src = imagesPath + "button_left_xon.jpg";
	preloads[1] = new Image(); preloads[1].src = imagesPath + "button_right_xon.jpg";
	preloads[2] = new Image(); preloads[2].src = imagesPath + "input_left_xon.gif";
	preloads[3] = new Image(); preloads[3].src = imagesPath + "input_right_xon.gif";
}

function getElements() {
	var re = new RegExp('(^| )'+'niceform'+'( |$)');
	for (var nf = 0; nf < document.getElementsByTagName('form').length; nf++) {
		if(re.test(niceforms[nf].className)) {
			for(var nfi = 0; nfi < document.forms[nf].getElementsByTagName('input').length; nfi++) {inputs.push(document.forms[nf].getElementsByTagName('input')[nfi]);}
			for(var nfl = 0; nfl < document.forms[nf].getElementsByTagName('label').length; nfl++) {labels.push(document.forms[nf].getElementsByTagName('label')[nfl]);}
		}
	}
}

function separateElements() {
	var r = 0; var c = 0; var t = 0; var rl = 0; var cl = 0; var tl = 0; var b = 0;
	for (var q = 0; q < inputs.length; q++) {
		if((inputs[q].type == "text") || (inputs[q].type == "password")) {texts[t] = inputs[q]; ++t;}
		if((inputs[q].type == "submit") || (inputs[q].type == "button")) {buttons[b] = inputs[q]; ++b;}
	}
}
function replaceTexts() {
	for(var q = 0; q < texts.length; q++) {
		texts[q].style.width = texts[q].size * 10 + 'px';
		txtLeft = document.createElement('img'); txtLeft.src = imagesPath + "input_left.gif"; txtLeft.className = "inputCorner";
		txtRight = document.createElement('img'); txtRight.src = imagesPath + "input_right.gif"; txtRight.className = "inputCorner";
		texts[q].parentNode.insertBefore(txtLeft, texts[q]);
		texts[q].parentNode.insertBefore(txtRight, texts[q].nextSibling);
		texts[q].className = "textinput";
		//create hovers
		texts[q].onfocus = function() {
			this.className = "textinputHovered";
			this.previousSibling.src = imagesPath + "input_left_xon.gif";
			this.nextSibling.src = imagesPath + "input_right_xon.gif";
		}
		texts[q].onblur = function() {
			this.className = "textinput";
			this.previousSibling.src = imagesPath + "input_left.gif";
			this.nextSibling.src = imagesPath + "input_right.gif";
		}
	}
}
function replaceTextareas() {
	for(var q = 0; q < textareas.length; q++) {
		var where = textareas[q].parentNode;
		var where2 = textareas[q].previousSibling;
		textareas[q].style.width = textareas[q].cols * 10 + 'px';
		textareas[q].style.height = textareas[q].rows * 10 + 'px';
		//create divs
		var container = document.createElement('div');
		container.className = "txtarea";
		container.style.width = textareas[q].cols * 10 + 20 + 'px';
		container.style.height = textareas[q].rows * 10 + 20 + 'px';
		var topRight = document.createElement('div');
		topRight.className = "tr";
		var topLeft = document.createElement('img');
		topLeft.className = "txt_corner";
		topLeft.src = imagesPath + "txtarea_tl.gif";
		var centerRight = document.createElement('div');
		centerRight.className = "cntr";
		var centerLeft = document.createElement('div');
		centerLeft.className = "cntr_l";
		if(!this.ie) {centerLeft.style.height = textareas[q].rows * 10 + 10 + 'px';}
		else {centerLeft.style.height = textareas[q].rows * 10 + 12 + 'px';}
		var bottomRight = document.createElement('div');
		bottomRight.className = "br";
		var bottomLeft = document.createElement('img');
		bottomLeft.className = "txt_corner";
		bottomLeft.src = imagesPath + "txtarea_bl.gif";
		//assemble divs
		container.appendChild(topRight);
		topRight.appendChild(topLeft);
		container.appendChild(centerRight);
		centerRight.appendChild(centerLeft);
		centerRight.appendChild(textareas[q]);
		container.appendChild(bottomRight);
		bottomRight.appendChild(bottomLeft);
		//insert structure
		where.insertBefore(container, where2);
		//create hovers
		textareas[q].onfocus = function() {
			this.previousSibling.className = "cntr_l_xon";
			this.parentNode.className = "cntr_xon";
			this.parentNode.previousSibling.className = "tr_xon";
			this.parentNode.previousSibling.getElementsByTagName("img")[0].src = imagesPath + "txtarea_tl_xon.gif";
			this.parentNode.nextSibling.className = "br_xon";
			this.parentNode.nextSibling.getElementsByTagName("img")[0].src = imagesPath + "txtarea_bl_xon.gif";
		}
		textareas[q].onblur = function() {
			this.previousSibling.className = "cntr_l";
			this.parentNode.className = "cntr";
			this.parentNode.previousSibling.className = "tr";
			this.parentNode.previousSibling.getElementsByTagName("img")[0].src = imagesPath + "txtarea_tl.gif";
			this.parentNode.nextSibling.className = "br";
			this.parentNode.nextSibling.getElementsByTagName("img")[0].src = imagesPath + "txtarea_bl.gif";
		}
	}
}
function buttonHovers() {
	for (var i = 0; i < buttons.length; i++) {
		buttons[i].className = "buttonSubmit";
		var buttonLeft = document.createElement('img');
		buttonLeft.src = imagesPath + "button_left.jpg";
		buttonLeft.className = "buttonImg";
		buttons[i].parentNode.insertBefore(buttonLeft, buttons[i]);
		var buttonRight = document.createElement('img');
		buttonRight.src = imagesPath + "button_right.jpg";
		buttonRight.className = "buttonImg";
		if(buttons[i].nextSibling) {buttons[i].parentNode.insertBefore(buttonRight, buttons[i].nextSibling);}
		else {buttons[i].parentNode.appendChild(buttonRight);}
		buttons[i].onmouseover = function() {
			this.className += "Hovered";
			this.previousSibling.src = imagesPath + "button_left_xon.jpg";
			this.nextSibling.src = imagesPath + "button_right_xon.jpg";
		}
		buttons[i].onmouseout = function() {
			this.className = this.className.replace(/Hovered/g, "");
			this.previousSibling.src = imagesPath + "button_left.jpg";
			this.nextSibling.src = imagesPath + "button_right.jpg";
		}
	}
}
//Useful functions
function findPosY(obj) {
	var posTop = 0;
	while (obj.offsetParent) {posTop += obj.offsetTop; obj = obj.offsetParent;}
	return posTop;
}
function findPosX(obj) {
	var posLeft = 0;
	while (obj.offsetParent) {posLeft += obj.offsetLeft; obj = obj.offsetParent;}
	return posLeft;
}

window.onload = init;