function newAlert(icon, type, text, time, dismiss){

	setTimeout(() => {
		$('#alertDIV').show();
	}, 10);
				
	//TIPOS DE ICONE
	if(icon == 'check'){
		icon = '<i class="fas fa-check"></i>';
	}
	if(icon == 'exclamation'){
		icon = '<i class="fas fa-exclamation"></i>';
	}
	if(icon == 'triangle'){
		icon = '<i class="fas fa-exclamation-triangle"></i>';
	}
	if(icon == 'exclamation-c'){
		icon = '<i class="fas fa-exclamation-circle"></i>';
	}
	if(icon == 'bell'){
		icon = '<i class="fas fa-bell"></i>';
	}
	if(icon == 'bell-slash'){
		icon = '<i class="fas fa-bell-slash"></i>';
	}
	if(icon == 'block'){
		icon = '<i class="fas fa-ban"></i>';
	}
	if(icon == 'comment'){
		icon = '<i class="fas fa-comment"></i>';
	}
	if(icon == 'comments'){
		icon = '<i class="fas fa-comments"></i>';
	}
	if(icon == 'times'){
		icon = '<i class="fas fa-times"></i>';
	}

	//TIPOS DE ALERTA
	if(type == 'warning'){
		$('#alertDIV').css('background-color','rgba(255, 182, 0)');
	}
	if(type == 'danger'){
		$('#alertDIV').css('background-color','rgba(255, 28, 28)');
	}
	if(type == 'success'){
		$('#alertDIV').css('background-color','rgba(54, 188, 68)');
	}
	if(type == 'grey'){
		$('#alertDIV').css('background-color','rgba(213, 219, 229)');
		$('#content').css('color','rgb(22, 22, 22)');
	}
	if(type == 'dark'){
		$('#alertDIV').css('background-color','rgba(0, 0, 0)');
	}


	//BOTAO DE FECHAR

	var tipo = typeof time;

	if(tipo == 'boolean'){
		dismiss = time;
		time = 0;
	}

	if(dismiss == false){
		$('#close').hide();
	}
				
	var tempo = time * 1000;

	if(tempo != 0){
		setTimeout(function() { 
			$('#alertDIV').hide();
		}, tempo);
	}else{
		setTimeout(function() { 
			$('#alertDIV').hide();
		}, 15000);
	}
	
	$('#icon').html(icon);
	$('#text').html(text);

}

function closeAlert(){
    $('#alertDIV').hide();
}
