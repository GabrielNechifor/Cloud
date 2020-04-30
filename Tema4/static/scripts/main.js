//Initiate jQuery on load.
$(function() {
    //Translate text with flask route   
    $("#analysis").on("click", function(e) {
      e.preventDefault();
      var translateVal = document.getElementById("text-to-translate").value;
      var translateRequest = { 'text': translateVal }
  
      if (translateVal !== "") {
        $.ajax({
          url: '/sentiment-text',
          method: 'POST',
          headers: {
              'Content-Type':'application/json'
          },
          dataType: 'json',
          data: JSON.stringify(translateRequest),
          success: function(data) {
            for (var i = 0; i < data.length; i++) {
              document.getElementById("document-sentiment").textContent = data[i].Document_Sentiment
              if (document.getElementById("document-sentiment").textContent !== ""){
                document.getElementById("sentiment").style.display = "block";
              }
              document.getElementById("posscore").textContent = data[i].Overall_scores.positive;
              document.getElementById("neuscore").textContent = data[i].Overall_scores.neutral;
              document.getElementById("negscore").textContent = data[i].Overall_scores.negative;
              /*var parsed = "Sentences\n";
              for (var j = 0; j < data[i].Sentences.length; j++){
                parsed += data[i].Sentences[j].Sentiment + "\n";
              }
              document.getElementById("sentences").innerHTML = parsed ; */
            }
          }
        });
      };
    });
    $("#translate").on("click", function(e) {
      e.preventDefault();
      var translateVal = document.getElementById("text-to-translate").value;
      var languageVal = document.getElementById("select-language").value;
      var translateRequest = { 'text': translateVal, 'to': languageVal }
  
      if (translateVal !== "") {
        $.ajax({
          url: '/translate-text',
          method: 'POST',
          headers: {
              'Content-Type':'application/json'
          },
          dataType: 'json',
          data: JSON.stringify(translateRequest),
          success: function(data) {
            for (var i = 0; i < data.length; i++) {
              document.getElementById("translation-result").textContent = data[i].translations[0].text;
              document.getElementById("detected-language-result").textContent = data[i].detectedLanguage.language;
              if (document.getElementById("detected-language-result").textContent !== ""){
                document.getElementById("detected-language").style.display = "block";
              }
              document.getElementById("confidence").textContent = data[i].detectedLanguage.score;
            }
          }
        });
      };
    });   
  })