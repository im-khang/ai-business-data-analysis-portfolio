window.portfolioCases = [
  {
    id: 'favorita-demand',
    eyebrow: 'Demand planning case',
    title: 'Favorita Planner Exception Queue',
    question: 'Which item/store/family combinations deserve planner attention first?',
    summary: 'Baseline forecasts become planner-review candidates using WAPE, MAE, Bias %, Forecast Score, FVA, ABC/XYZ segmentation, and assumption-based safety stock / reorder point logic.',
    proof: ['Forecast metrics', 'Planner queue', 'Assumption caveats'],
    links: [
      {label: 'Dashboard', href: 'demand-forecasting-replenishment/'},
      {label: 'Case study', href: 'https://github.com/im-khang/ai-business-data-analysis-portfolio/tree/master/case-studies/demand-forecasting-replenishment'},
      {label: 'Build metadata', href: 'demand-forecasting-replenishment/assets/data/build_metadata.json'},
      {label: 'Code', href: 'https://github.com/im-khang/ai-business-data-analysis-portfolio/tree/master/case-studies/demand-forecasting-replenishment'}
    ]
  },
  {
    id: 'olist-sla',
    eyebrow: 'Delivery operations case',
    title: 'Olist Delivery SLA Risk',
    question: 'Which delivery SLA risks deserve operations attention first?',
    summary: 'Late-delivery exposure, review-score association, and seller/category/region investigation candidates framed for practical operations triage without unsupported root-cause claims.',
    proof: ['96,470 delivered orders', '6.77% late rate', 'Candidate ranking'],
    links: [
      {label: 'Dashboard', href: 'inventory-stockout-overstock-analysis/'},
      {label: 'Case study', href: 'https://github.com/im-khang/ai-business-data-analysis-portfolio/blob/master/case-studies/inventory-stockout-overstock-analysis/README.md'},
      {label: 'SLA summary', href: 'https://github.com/im-khang/ai-business-data-analysis-portfolio/blob/master/case-studies/inventory-stockout-overstock-analysis/artifacts/delivery-sla-summary.md'},
      {label: 'Candidate ranking', href: 'https://github.com/im-khang/ai-business-data-analysis-portfolio/blob/master/case-studies/inventory-stockout-overstock-analysis/artifacts/seller-category-region-risk.md'},
      {label: 'Code', href: 'https://github.com/im-khang/ai-business-data-analysis-portfolio/tree/master/case-studies/inventory-stockout-overstock-analysis'}
    ]
  }
];
