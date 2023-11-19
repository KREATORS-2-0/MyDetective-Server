'''
Run the lie_analyzer class and the data obtained from it through
the ML model.
'''


from lie_analyzer import LieAnalyzer

if __name__ == "__main__":
    analyzer = LieAnalyzer()
    try:
        analyzer.start_streaming()
        for _ in range(1000):
            analyzer.append_data()
        analyzer.stop_streaming()
        analyzer.analyze()
        print(f'{analyzer.analysis_result} : {analyzer.analysis_confidence * 100}')
    except :
        analyzer.stop_streaming()
    finally:
        analyzer.stop_streaming()