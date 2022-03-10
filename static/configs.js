function getData() {
    //============================== JĘZYKI ===========================
    const recommend_data = {
      labels: recommend.items,
      datasets: [
        {
          label: "Języki",
          data: recommend.count,
          backgroundColor: [
            "#FFD878",
            "#FFB368",
            "#EB7360",
            "#FF8A91",
            "#FFD3AA",
            "#FF8422",
            "#FFB5B9",
          ],
          borderColor: [
            "#FFC43C",
            "#FF9A4A",
            "#FF6E64",
            "#FF5E74",
            "#FFB77A",
            "#FF6B00",
            "#FF8C90",
          ],
          borderWidth: 2,
        },
      ],
    };
  
    const recommend_config = {
      type: "pie",
      data: recommend_data,
  
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {},
      },
    };
  
    return {
      recommend: recommend_config,
    };
  }
  