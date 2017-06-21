function equalHeight(group) {    
    var tallest = 0;    
    group.each(function() {       
        var thisHeight = $(this).height();       
        if(thisHeight > tallest) {          
            tallest = thisHeight;       
        }    
    });    
    group.each(function() { $(this).height(tallest); });
} 

$(document).ready(function() {
	//window.alert('wow'); 
    //this function to get the user input value and will calculate final price!
    //$("#hotdog").keydown(function (e){
        //first we pick if the entered char is numeric
      //  if(e.keyCode == 13 || e.keyCode == 8 || (e.keyCode >= 48 && e.keyCode <= 57)){
            //we change value in total cost label!
        //}else{
          //  $(this).html('Entra um numero!');
        //}
    //});
    //window.alert('initial');
    $('#seetrans').click(function(){
        //change display style
        if (document.getElementById('uploaded').style.display == 'none'){
            document.getElementById('uploaded').style.display = 'block';
            document.getElementById('seetrans').innerHTML = "Esconder as transacoes carregadas";
        }else{
            document.getElementById('uploaded').style.display = 'none';
            document.getElementById('seetrans').innerHTML = "Mostrar as transacoes carregadas";
        }
        //x.style.display = 'block';
    });
    var hotValue = document.getElementById("hotdog").value;
    var pipValue = document.getElementById("pipoca").value;
    var pamValue = document.getElementById("pamonha").value;
    var quantiteHot = parseInt(hotValue,10);
    var quantitePip = parseInt(pipValue,10);
    var quantitePam = parseInt(pamValue,10);
    var totalCost = (0.001*(quantiteHot + quantitePam) + 0.002*quantitePip).toFixed(3);
    var finalCost = totalCost.toString();
    document.getElementById("totalCost").innerHTML = finalCost + "Btc";
    $('#hotdog').on('change', function(){
        var hotValue = document.getElementById("hotdog").value;
        var pipValue = document.getElementById("pipoca").value;
        var pamValue = document.getElementById("pamonha").value;
        //get totalCost
        var quantiteHot = parseInt(hotValue,10);
        var quantitePip = parseInt(pipValue,10);
        var quantitePam = parseInt(pamValue,10);
        var totalCost = (0.001*(quantiteHot + quantitePam) + 0.002*quantitePip).toFixed(3);
        var finalCost = totalCost.toString();
        document.getElementById("totalCost").innerHTML = finalCost + "Btc";
        document.getElementById("hiddenCost").value = finalCost;
        
    });

    $('#pipoca').on('change', function(){
        var hotValue = document.getElementById("hotdog").value;
        var pipValue = document.getElementById("pipoca").value;
        var pamValue = document.getElementById("pamonha").value;
        //get totalCost
        var quantiteHot = parseInt(hotValue,10);
        var quantitePip = parseInt(pipValue,10);
        var quantitePam = parseInt(pamValue,10);
        var totalCost = (0.001*(quantiteHot + quantitePam) + 0.002*quantitePip).toFixed(3);
        var finalCost = totalCost.toString();
        document.getElementById("totalCost").innerHTML = finalCost + "Btc";
        document.getElementById("hiddenCost").value = finalCost;
    });

    $('#pamonha').on('change', function(){
        var hotValue = document.getElementById("hotdog").value;
        var pipValue = document.getElementById("pipoca").value;
        var pamValue = document.getElementById("pamonha").value;
        //get totalCost
        var quantiteHot = parseInt(hotValue,10);
        var quantitePip = parseInt(pipValue,10);
        var quantitePam = parseInt(pamValue,10);
        var totalCost = (0.001*(quantiteHot + quantitePam) + 0.002*quantitePip).toFixed(3);
        var finalCost = totalCost.toString();
        document.getElementById("totalCost").innerHTML = finalCost + "Btc";  
        document.getElementById("hiddenCost").value = finalCost;  
    });

    $('.productImage').click(function(){
        //create address to be copied
        var aux = document.createElement("input");
        aux.setAttribute("value", document.getElementById("pubKeyValue").innerHTML);
        document.body.appendChild(aux);
        aux.select();
        document.execCommand("copy")
        var alertText = "O endereco do comerciante" + " " + document.getElementById("pubKeyValue").innerHTML + " foi copiado!";
        window.alert(alertText);
        document.body.removeChild(aux);

    });



    //equalHeight($(".thumbnail"));
    //var qrcode = new QRCode("qrcode");
    //function makeCode() {
      //  var qrText = document.getElementById("pubkey");
        //window.alert('entered here');
       // qrcode.makeCode(qrText.value);
    //}
    //makeCode();
});


