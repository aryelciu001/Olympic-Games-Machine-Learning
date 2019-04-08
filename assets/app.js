setTimeout(()=>{
	/////////////////////////////////
	const heightBoxPlot = document.getElementById('height-boxplot');
	const weightBoxPlot = document.getElementById('weight-boxplot');
	const ageBoxPlot = document.getElementById('age-boxplot');
	const boxPlots = [heightBoxPlot, weightBoxPlot, ageBoxPlot];
	const option = document.getElementsByClassName('title-opt');
	for (var i = 0; i < option.length; i++) {

			option[i].addEventListener('click', (e) => {
				if(!e.target.classList.contains('title-active')){
					for (var i = 0; i < option.length; i++) {
						boxPlots[i].classList.remove('active');
						if(option[i].classList.contains('title-active')){
							option[i].classList.toggle('title-active');
						}
					}
					e.target.classList.toggle('title-active');
					if(e.target.classList.contains('height')){
						heightBoxPlot.classList.add('active');
					}else if(e.target.classList.contains('weight')){
						weightBoxPlot.classList.add('active');
					}else if(e.target.classList.contains('age')){
						ageBoxPlot.classList.add('active');
					}
				}
			})
		}
	/////////////////////////////////
	
},3000)