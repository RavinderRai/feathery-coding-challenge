import pytest
from form.pdf_extraction_pipeline.run_pipeline import run_pipeline

def test_run_pipeline_with_sample_pdf():
    sample_pdf_path = 'form/pdf_extraction_pipeline/tests/sample-new-fidelity-acnt-stmt.pdf'
    
    with open(sample_pdf_path, 'rb') as pdf_file:
        results = run_pipeline(pdf_file)

    assert isinstance(results, list)

    # Extract individual components for type verification
    account_owner_name_result = results[0].get('Account owner name')
    portfolio_value_result = results[1].get('Portfolio value')
    cost_basis_responses = results[2].get('Name and cost basis of each holding')

    assert isinstance(account_owner_name_result, str), "'Account owner name' should be a string."
    assert isinstance(portfolio_value_result, str), "'Portfolio value' should be a string."
    assert isinstance(cost_basis_responses, list), "'Name and cost basis of each holding' should be a list."
    for item in cost_basis_responses:
        assert isinstance(item, dict), "Each item in 'Name and cost basis of each holding' should be a dictionary."
